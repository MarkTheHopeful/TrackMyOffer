package cub.trackmyoffer

import EducationEntry
import ExperienceEntry
import ProfileData
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.sessions.*
import kotlinx.serialization.Serializable
import kotlinx.serialization.SerializationException
import kotlinx.serialization.json.Json


@Serializable
data class ExportResponse(
    val profile: ProfileData?,
    val education: List<EducationEntry>,
    val experience: List<ExperienceEntry>,
)

inline fun <reified T> decodeJson(json : String, defaultValue: T): T = try {
    Json.decodeFromString<T>(json)
} catch (e : SerializationException) {
    println("Failed to parse: ${e.message}")
    defaultValue
}

fun checkResponse(response: HttpResponse) {
    if (!response.status.isSuccess()) {
        throw Exception(response.status.description)
    }
}

fun Route.userRouting(httpClient: HttpClient, utilityDatabase: UtilityDatabase, config: FeatureProviderRoutingConfig) {

    suspend fun extractExportResponse(call: RoutingCall): ExportResponse {
        val userId = extractUserId(call, httpClient, utilityDatabase)

        val profileResponse: HttpResponse = httpClient.get("${config.remote}/api/profile/${userId}")
        checkResponse(profileResponse)

        val educationResponse: HttpResponse = httpClient.get("${config.remote}/api/${userId}/educations") {}
        checkResponse(educationResponse)

        val experienceResponse: HttpResponse = httpClient.get("${config.remote}/api/${userId}/experiences") {}
        checkResponse(experienceResponse)

        val profile = decodeJson<ProfileData?>(profileResponse.body(), null)
        val educations = decodeJson<List<EducationEntry>>(educationResponse.body(), emptyList())
        val experiences = decodeJson<List<ExperienceEntry>>(experienceResponse.body(), emptyList())

        return ExportResponse(
            profile,
            educations,
            experiences
        )
    }

    suspend fun deleteUser(call: RoutingCall) {
        val userId = extractUserId(call, httpClient, utilityDatabase)

        val userResponse = extractExportResponse(call)

        userResponse.education.forEach { educationEntry ->
            val response = httpClient.delete("${config.remote}/api/profile/${userId}/education/${educationEntry.id}")
            checkResponse(response)
        }

        userResponse.experience.forEach { experienceEntry ->
            val response = httpClient.delete("${config.remote}/api/${userId}/experiences/${experienceEntry.id}")
            checkResponse(response)
        }

        val profileDeleteResponse = httpClient.delete("${config.remote}/api/profile/${userId}")
        checkResponse(profileDeleteResponse)

        call.sessions.clear<UserSession>()
    }

    route("/user") {
        get("/export") {
            try {
                val exportResponse = extractExportResponse(call)
                call.respond(HttpStatusCode.OK, exportResponse)
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, e.message ?: "Unknown error")
            }
        }

        delete("/delete") {
            try {
                deleteUser(call)
                call.respond(
                    HttpStatusCode.OK,
                    mapOf("message" to "Profile successfully deleted!")
                )
            } catch (e: Exception) {
                call.respond(HttpStatusCode.InternalServerError, mapOf("message" to (e.message ?: "Unknown error")))
            }
        }
    }
}

