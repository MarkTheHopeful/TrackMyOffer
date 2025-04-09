package cub.trackmyoffer

import io.ktor.http.*
import io.ktor.server.plugins.*
import io.ktor.server.plugins.cors.routing.*
import io.ktor.server.plugins.swagger.*
import io.ktor.server.response.*
import io.ktor.server.routing.*

fun Route.backendRouting() {
    route("/v0") {
        get("/") {
            call.respondText("Hello World!")
        }

        get("/hello") {
            call.respondText("Hello, ${call.request.origin}")
        }

        swaggerUI(path = "swagger", swaggerFile = "openapi.yaml") {

        }
    }
}
