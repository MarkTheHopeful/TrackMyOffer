package cub.trackmyoffer

import CoverLetterRequest
import CvGenerationRequest
import EducationEntry
import ExperienceEntry
import ProfileData
import WithJobDescription
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.sessions.*
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put

data class Response(val status: HttpStatusCode, val body: String)

data class FeatureProviderRoutingConfig(val remote: String)

fun Route.featureProviderRouting(httpClient: HttpClient, config: FeatureProviderRoutingConfig, utilityDatabase: UtilityDatabase) {

    suspend fun getJobDescription(jobDescription: String): Response {
        val response = httpClient.post("${config.remote}/api/extract-job-description") {
            contentType(ContentType.Application.Json)
            setBody(buildJsonObject {
                put("jobDescription", jobDescription)
            }.toString())
        }
        return Response(response.status, response.bodyAsText())
    }

    suspend fun extractJobDescription(call: RoutingCall): Response {
        val jobDescription = call.receive<WithJobDescription>().jobDescription
        return getJobDescription(jobDescription)
    }
    
    fun Route.baseFeatureProviderRouting(userIdSupplier: suspend RoutingContext.() -> Int) {
        get("/hello") {
            val name = call.parameters["name"]
            if (name == null) {
                call.respondText("Missing name parameter", status = HttpStatusCode.BadRequest)
                return@get
            }

            val response = httpClient.post("${config.remote}/greet") {
                contentType(ContentType.Application.Json)
                setBody(buildJsonObject {
                    put("name", name)
                }.toString())
            }
            call.respondText(response.bodyAsText(), status = response.status)
        }

        get("/") {
            val response = httpClient.get("${config.remote}/")
            call.respondText(response.bodyAsText(), status = response.status)
        }

        post("/profile") {
            val profileReq = call.receive<ProfileData>()

            profileReq.id = userIdSupplier()

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
            val userId = userIdSupplier()

            val remoteResponse: HttpResponse = httpClient.get("${config.remote}/api/profile/${userId}")

            call.respond(
                status = remoteResponse.status,
                message = remoteResponse.bodyAsText()
            )
        }

        post("/profile/education") {
            val educationReq = call.receive<EducationEntry>()

            val userId = userIdSupplier()

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

        get("/profile/education") {
            val userId = userIdSupplier()

            val remoteResponse: HttpResponse = httpClient.get("${config.remote}/api/${userId}/educations") {}

            val text = remoteResponse.bodyAsText()
            call.respond(
                status = remoteResponse.status,
                message = text
            )
        }

        delete("/profile/education") {
            val userId = userIdSupplier()
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

            val userId = userIdSupplier()
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
            val userId = userIdSupplier()

            val remoteResponse: HttpResponse = httpClient.get("${config.remote}/api/${userId}/experiences") {}

            val text = remoteResponse.bodyAsText()
            call.respond(
                status = remoteResponse.status,
                message = text
            )
        }

        delete("/profile/experience") {
            val userId = userIdSupplier()
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

        post("/build-cv") {
            val cvRequest = call.receive<CvGenerationRequest>()
            val extractorResponse = getJobDescription(cvRequest.jobDescription)
            if (extractorResponse.status != HttpStatusCode.OK) {
                call.respond(extractorResponse.status, extractorResponse.body)
                return@post
            }

            val profileId = userIdSupplier()

            val response = httpClient.post("${config.remote}/api/build-cv") {
                contentType(ContentType.Application.Json)
                setBody(
                    extractorResponse.body
                )
                parameter("profile_id", profileId)
                cvRequest.region?.takeIf { it.isNotBlank() }?.let { parameter("region", it) }
            }
            call.respondText(response.bodyAsText(), status = response.status)
        }

        post("/match-position") {
            val extractorResponse = extractJobDescription(call)
            if (extractorResponse.status != HttpStatusCode.OK) {
                call.respond(extractorResponse.status, extractorResponse.body)
                return@post
            }

            val profileId = userIdSupplier()

            val response = httpClient.post("${config.remote}/api/match-position") {
                contentType(ContentType.Application.Json)
                setBody(
                    extractorResponse.body
                )
                parameter("profile_id", profileId)
            }
            call.respondText(response.bodyAsText(), status = response.status)
        }

        post("/cover-letter") {
            val request = call.receive<CoverLetterRequest>()
            val extractorResponse = getJobDescription(request.jobDescription)
            if (extractorResponse.status != HttpStatusCode.OK) {
                call.respond(extractorResponse.status, extractorResponse.body)
                return@post
            }

            val profileId = userIdSupplier()

            val textStyle = call.request.queryParameters["textStyle"]
            val notes = call.request.queryParameters["notes"]

            val response = httpClient.post("${config.remote}/api/generate-cover-letter") {
                contentType(ContentType.Application.Json)
                setBody(
                    extractorResponse.body
                )
                parameter("profile_id", profileId)
                parameter("style", textStyle)
                parameter("notes", notes)
            }
            call.respondText(response.bodyAsText(), status = response.status)
        }

        post("/analyze-gaps") {
            val profileId = userIdSupplier()

            val extractorResponse = extractJobDescription(call)
            if (extractorResponse.status != HttpStatusCode.OK) {
                call.respond(extractorResponse.status, extractorResponse.body)
                return@post
            }

            val response = httpClient.post("${config.remote}/api/analyze-gaps") {
                contentType(ContentType.Application.Json)
                setBody(
                    extractorResponse.body
                )
                parameter("profile_id", profileId)
            }
            call.respondText(response.bodyAsText(), status = response.status)
        }
    }

    route("/features") {
        route("/v0") {
            route("/DEBUG") {
                if (environment.config.propertyOrNull("ktor.deployment.debug")?.getString()?.toBooleanStrictOrNull() == true) {
                    baseFeatureProviderRouting { 1 } // debug routes always use 1 as profile id
                }
            }

            baseFeatureProviderRouting { extractUserId(call, httpClient, utilityDatabase) }
        }
    }
}
