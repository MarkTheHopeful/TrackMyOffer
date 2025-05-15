package cub.trackmyoffer

import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.transaction
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import com.zaxxer.hikari.HikariConfig
import com.zaxxer.hikari.HikariDataSource
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import kotlinx.serialization.json.*
import io.ktor.server.application.*
import kotlinx.serialization.Serializable
import EducationEntry
import ExperienceEntry
import ProfileData

/**
 * Table for storing the correspondence between Google emails and profile IDs.
 */
object UserProfiles : Table() {
    val email = varchar("email", 255).uniqueIndex()
    val profileId = integer("profile_id")

    override val primaryKey = PrimaryKey(email)
}

/**
 * UtilityDatabase class for managing user profile mappings.
 * This database maintains the correspondence between Google emails and profile IDs.
 */
class UtilityDatabase(private val httpClient: HttpClient, private val featureProviderUrl: String) {

    /**
     * Initializes the database connection and creates the necessary tables.
     */
    fun init() {
        // Get database connection parameters from environment variables or use defaults
        val dbHost = System.getenv("DB_HOST") ?: "utility_db"
        val dbPort = System.getenv("DB_PORT") ?: "5432"
        val dbName = System.getenv("DB_NAME") ?: "utility_db"
        val dbUser = System.getenv("DB_USER") ?: "utility_user"
        val dbPassword = System.getenv("DB_PASSWORD") ?: "utility_password"

        val config = HikariConfig().apply {
            driverClassName = "org.postgresql.Driver"
            jdbcUrl = "jdbc:postgresql://$dbHost:$dbPort/$dbName"
            username = dbUser
            password = dbPassword
            maximumPoolSize = 10
            isAutoCommit = false
            transactionIsolation = "TRANSACTION_REPEATABLE_READ"
            validate()
        }

        try {
            val dataSource = HikariDataSource(config)
            Database.connect(dataSource)

            transaction {
                // We don't need to create tables here as they are created by the initialization script
                // But we can verify that they exist
                if (!UserProfiles.exists()) {
                    throw RuntimeException("UserProfiles table does not exist. Database initialization may have failed.")
                }
            }
        } catch (e: Exception) {
            println("Error connecting to database: ${e.message}")
            // Fall back to H2 in-memory database for development/testing
            val h2Config = HikariConfig().apply {
                driverClassName = "org.h2.Driver"
                jdbcUrl = "jdbc:h2:mem:utility_database;DB_CLOSE_DELAY=-1"
                maximumPoolSize = 10
                isAutoCommit = false
                transactionIsolation = "TRANSACTION_REPEATABLE_READ"
                validate()
            }

            val h2DataSource = HikariDataSource(h2Config)
            Database.connect(h2DataSource)

            transaction {
                SchemaUtils.create(UserProfiles)
            }

            println("Connected to fallback H2 in-memory database")
        }
    }

    /**
     * Gets the profile ID for a given email.
     * If the email is not found in the database, creates a new profile and stores the association.
     * 
     * @param email The Google email address
     * @param userInfo The user information from Google OAuth
     * @return The profile ID
     */
    suspend fun getOrCreateProfileId(email: String, userInfo: UserInfo): Int {
        // Check if the email exists in the database
        val existingProfileId = transaction {
            UserProfiles.selectAll().where { UserProfiles.email eq email }
                .map { it[UserProfiles.profileId] }
                .singleOrNull()
        }

        // If the email exists, return the profile ID
        if (existingProfileId != null) {
            return existingProfileId
        }

        // If the email doesn't exist, create a new profile
        val newProfileId = createNewProfile(userInfo)

        // Store the association in the database
        transaction {
            UserProfiles.insert {
                it[UserProfiles.email] = email
                it[profileId] = newProfileId
            }
        }

        return newProfileId
    }

    /**
     * Creates a new profile in the feature provider.
     * 
     * @param userInfo The user information from Google OAuth
     * @return The newly created profile ID
     */
    private suspend fun createNewProfile(userInfo: UserInfo): Int {
        // Create a minimal profile with information from Google OAuth
        val profileData = ProfileData(
            id = null, // This will be assigned by the feature provider
            firstName = userInfo.givenName,
            lastName = userInfo.familyName,
            email = userInfo.email,
            phone = null,
            country = null,
            state = null,
            city = null,
            linkedinUrl = null,
            githubUrl = null,
            personalWebsite = null,
            otherUrl = null,
            aboutMe = null
        )

        // Send the POST request to create a new profile
        val response = httpClient.post("$featureProviderUrl/api/profile") {
            contentType(ContentType.Application.Json)
            setBody(profileData)
        }

        // Parse the response to get the profile ID
        val responseBody = response.bodyAsText()
        val jsonObject = Json.parseToJsonElement(responseBody).jsonObject

        // Extract the profile ID from the response
        return jsonObject["id"]?.jsonPrimitive?.int
            ?: throw RuntimeException("Failed to create new profile: $responseBody")
    }
}
