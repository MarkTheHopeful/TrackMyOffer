package cub.trackmyoffer

import EducationEntry
import ExperienceEntry
import ProfileData
import io.ktor.client.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.sessions.*
import kotlinx.serialization.Serializable


@Serializable
data class ExportResponse(
    val profile: ProfileData?,
    val education: List<EducationEntry>,
    val experience: List<ExperienceEntry>,
    val message: String = "Data export successful"
)

fun Route.userRouting(httpClient: HttpClient, utilityDatabase: UtilityDatabase) {
    route("/user") {
        get("/export") {
            val userSession: UserSession = call.sessions.get() ?: run {
                call.respond(HttpStatusCode.Unauthorized, mapOf("error" to "Not authenticated"))
                return@get
            }

            val userInfo = getUserInfo(httpClient, userSession)
            val profileId = utilityDatabase.getOrCreateProfileId(userInfo.email, userInfo)

            call.respond(
                HttpStatusCode.OK,
                ExportResponse(
                    profile = null,
                    education = emptyList(),
                    experience = emptyList(),
                    message = "Export endpoint - to be implemented"
                )
            )
        }

        delete("/delete") {
            val userSession: UserSession = call.sessions.get() ?: run {
                call.respond(HttpStatusCode.Unauthorized, mapOf("error" to "Not authenticated"))
                return@delete
            }

            val userInfo = getUserInfo(httpClient, userSession)
            val profileId = utilityDatabase.getOrCreateProfileId(userInfo.email, userInfo)

            call.sessions.clear<UserSession>()

            call.respond(
                HttpStatusCode.OK,
                mapOf("message" to "Delete endpoint - to be implemented")
            )
        }
    }
}

