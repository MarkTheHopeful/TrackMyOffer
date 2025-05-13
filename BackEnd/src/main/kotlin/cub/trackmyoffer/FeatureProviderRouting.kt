package cub.trackmyoffer

import EducationEntry
import ExperienceEntry
import ProfileData
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.sessions.*

data class Response(val status: HttpStatusCode, val body: String)

data class FeatureProviderRoutingConfig(val remote: String)

fun Route.featureProviderRouting(httpClient: HttpClient, config: FeatureProviderRoutingConfig) {
    suspend fun extractUserId(call: RoutingCall): Int {
        val userSession: UserSession =
            call.sessions.get() ?: throw RuntimeException("Invalid session during request")

        if (!validateToken(httpClient, userSession)) {
            application.log.debug("Invalid or expired session, redirecting to login")
            call.sessions.clear<UserSession>()
            call.respondRedirect("/login")
        }
        val userInfo: UserInfo = getUserInfo(httpClient, userSession)
        // TODO: Go to the database and fetch user_id by the email
        return 1
    }

    suspend fun extractJobDescription(call: RoutingCall): Response {
        val jobDescriptionLink = call.request.queryParameters["jobDescription"]
            ?: return Response(HttpStatusCode.BadRequest, "Missing jobDescription parameter")
        val response = httpClient.post("${config.remote}/api/extract-job-description") {
            contentType(ContentType.Application.Json)
            setBody("""{"jobDescription": "$jobDescriptionLink"}""")
        }
        return Response(response.status, response.bodyAsText())
    }

    route("/features") {
        route("/v0") {
            get("/hello") {
                val name = call.parameters["name"]
                if (name == null) {
                    call.respondText("Missing name parameter", status = HttpStatusCode.BadRequest)
                    return@get
                }

                val response = httpClient.post("${config.remote}/greet") {
                    contentType(ContentType.Application.Json)
                    setBody("""{"name": "$name"}""")
                    // TODO: add serialization plugin & serialize properly
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }

            get("/") {
                val response = httpClient.get("${config.remote}/")
                call.respondText(response.bodyAsText(), status = response.status)
            }

            post("/profile") {
                val profileReq = call.receive<ProfileData>()

                profileReq.id = extractUserId(call)

                val remoteResponse: HttpResponse = httpClient.post("${config.remote}/api/profile") {
                    contentType(ContentType.Application.Json)
                    setBody(profileReq)
                }

                val text = remoteResponse.bodyAsText()
                call.respond(
                    status = remoteResponse.status,
                    message = text
                )
            }

            get("/profile") {
                val userId = extractUserId(call)

                val remoteResponse: HttpResponse = httpClient.get("${config.remote}/api/profile/${userId}")

                call.respond(
                    status = remoteResponse.status,
                    message = remoteResponse.bodyAsText()
                )
            }

            post("/profile/education") {
                val educationReq = call.receive<EducationEntry>()

                val userId = extractUserId(call)

                val remoteResponse: HttpResponse = httpClient.post("${config.remote}/api/profile/${userId}/education") {
                    contentType(ContentType.Application.Json)
                    setBody(educationReq)
                }

                val text = remoteResponse.bodyAsText()
                call.respond(
                    status = remoteResponse.status,
                    message = text
                )
            }

            delete("/profile/education/") {
                val userId = extractUserId(call)
                val educationId = call.parameters["educationId"]?.toIntOrNull()
                if (educationId == null) {
                    call.respondText("Missing education id parameter", status = HttpStatusCode.BadRequest)
                    return@delete
                }

                val remoteResponse: HttpResponse =
                    httpClient.delete("${config.remote}/api/profile/${userId}/education/${educationId}")

                call.respond(
                    status = remoteResponse.status,
                    message = remoteResponse.bodyAsText()
                )
            }

            post("/profile/experience") {
                val experienceReq = call.receive<ExperienceEntry>()

                val userId = extractUserId(call)
                experienceReq.profileId = userId

                val remoteResponse: HttpResponse = httpClient.post("${config.remote}/api/experience") {
                    contentType(ContentType.Application.Json)
                    setBody(experienceReq)
                }

                val text = remoteResponse.bodyAsText()
                call.respond(
                    status = remoteResponse.status,
                    message = text
                )
            }

            get("/profile/experience") {
                val userId = extractUserId(call)

                val remoteResponse: HttpResponse = httpClient.get("${config.remote}/api/${userId}/experiences") {}

                val text = remoteResponse.bodyAsText()
                call.respond(
                    status = remoteResponse.status,
                    message = text
                )
            }

            delete("/profile/experience") {
                val userId = extractUserId(call)
                val experienceId = call.parameters["experienceId"]?.toIntOrNull()
                if (experienceId == null) {
                    call.respondText("Missing experience id parameter", status = HttpStatusCode.BadRequest)
                    return@delete
                }

                val remoteResponse: HttpResponse =
                    httpClient.delete("${config.remote}/api/${userId}/experiences/${experienceId}")

                call.respond(
                    status = remoteResponse.status,
                    message = remoteResponse.bodyAsText()
                )
            }

            get("/match-position") {
                val extractorResponse = extractJobDescription(call)
                if (extractorResponse.status != HttpStatusCode.OK) {
                    call.respond(extractorResponse.status, extractorResponse.body)
                    return@get
                }

                val profileId = extractUserId(call)

                val response = httpClient.post("${config.remote}/api/match-position") {
                    contentType(ContentType.Application.Json)
                    setBody(
                        "${
                            extractorResponse.body.trimEnd().removeSuffix("}")
                        }, \"profileId\": ${profileId}}"
                    )
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }


            get("/build-cv") {
                val extractorResponse = extractJobDescription(call)
                if (extractorResponse.status != HttpStatusCode.OK) {
                    call.respond(extractorResponse.status, extractorResponse.body)
                    return@get
                }

                val profileId = extractUserId(call)

                val response = httpClient.post("${config.remote}/api/build-cv") {
                    contentType(ContentType.Application.Json)
                    setBody(
                        "${
                            extractorResponse.body.trimEnd().removeSuffix("}")
                        }, \"profileId\": ${profileId}}"
                    )
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }

            get("/generate-motivational-letter") {
                val extractorResponse = extractJobDescription(call)
                if (extractorResponse.status != HttpStatusCode.OK) {
                    call.respond(extractorResponse.status, extractorResponse.body)
                    return@get
                }

                val profileId = extractUserId(call)

                val textStyle = call.request.queryParameters["textStyle"]
                val notes = call.request.queryParameters["notes"]

                val response = httpClient.post("${config.remote}/api/generate-motivational-letter") {
                    contentType(ContentType.Application.Json)
                    setBody(
                        "${
                            extractorResponse.body.trimEnd().removeSuffix("}")
                        }${
                            if (textStyle != null) """, "textStyle": "$textStyle""""
                            else ""
                        }${
                            if (notes != null) """, "notes": "$notes""""
                            else ""
                        }, \"profileId\": ${profileId}}"
                    )
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }

            post("/cover-letter") {
                val request = call.receive<String>()
                val userId = extractUserId(call)
                val response = httpClient.post("${config.remote}/api/generate-cover-letter") {
                    contentType(ContentType.Application.Json)
                    setBody(request)
                    parameter("profile_id", userId)
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }
        }
    }
}
