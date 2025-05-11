package cub.trackmyoffer

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

data class Response(val status: HttpStatusCode, val body: String)

data class FeatureProviderRoutingConfig(val remoteHost: String, val remotePort: String) {
    val remote = "http://$remoteHost:$remotePort"
}

fun Route.featureProviderRouting(httpClient: HttpClient, config: FeatureProviderRoutingConfig) {
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

            suspend fun extractJobDescription(call: RoutingCall): Response {
                val jobDescription = call.request.queryParameters["jobDescriptionLink"]
                    ?: return Response(HttpStatusCode.BadRequest, "Missing jobDescriptionLink parameter")

                val response = httpClient.post("${config.remote}/extract-job-description") {
                    contentType(ContentType.Application.Json)
                    setBody("""{"jobDescription": "$jobDescription"}""")
                }
                return Response(response.status, response.bodyAsText())
            }

            get("/match-position") {
                val extractorResponse = extractJobDescription(call)
                if (extractorResponse.status != HttpStatusCode.OK) {
                    call.respond(extractorResponse.status, extractorResponse.body)
                    return@get
                }

                val response = httpClient.post("${config.remote}/match-position") {
                    contentType(ContentType.Application.Json)
                    setBody(extractorResponse.body)
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }


            get("/build-cv") {
                val extractorResponse = extractJobDescription(call)
                if (extractorResponse.status != HttpStatusCode.OK) {
                    call.respond(extractorResponse.status, extractorResponse.body)
                    return@get
                }

                val response = httpClient.post("${config.remote}/build-cv") {
                    contentType(ContentType.Application.Json)
                    setBody(extractorResponse.body)
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }

            get("/generate-motivational-letter") {
                val extractorResponse = extractJobDescription(call)
                if (extractorResponse.status != HttpStatusCode.OK) {
                    call.respond(extractorResponse.status, extractorResponse.body)
                    return@get
                }

                val textStyle = call.request.queryParameters["textStyle"]
                val notes = call.request.queryParameters["notes"]

                val response = httpClient.post("${config.remote}/generate-motivational-letter") {
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
                        }}"
                    )
                }
                call.respondText(response.bodyAsText(), status = response.status)
            }
        }
    }
}
