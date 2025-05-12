package cub.trackmyoffer

import ProfileRequest
import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

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

            post("/profile") {
                val profileReq = call.receive<ProfileRequest>()


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
        }
    }
}