package cub.trackmyoffer

import io.ktor.client.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

data class FeatureProviderRoutingConfig(val remoteHost: String, val remotePort: String) {
    val remote = "http://$remoteHost:$remoteHost"
}

fun Route.featureProviderRouting(httpClient: HttpClient, config: FeatureProviderRoutingConfig) {
    route("/features") {
        route("/v0") {
            get("/hello") {
                val response = httpClient.get("${config.remote}/greet")
                call.respondText(response.bodyAsText(), status = response.status)
            }
        }
    }
}