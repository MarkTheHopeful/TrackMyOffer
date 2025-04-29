package cub.trackmyoffer

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.logging.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.calllogging.*
import io.ktor.server.plugins.cors.routing.*
import io.ktor.server.routing.*

fun main(args: Array<String>) = EngineMain.main(args)

fun Application.module() {
    val fProviderHost = environment.config.propertyOrNull("ktor.feature_provider.host")?.getString() ?: "0.0.0.0"
    val fProviderPort = environment.config.propertyOrNull("ktor.feature_provider.port")?.getString() ?: "8081"

    val httpClient = HttpClient(CIO) {
        install(Logging) {
            logger = Logger.DEFAULT
            level = LogLevel.HEADERS
        }

        expectSuccess = false
        engine {
            requestTimeout = 10_000
        }
    }

    // TODO: setup cors properly
    install(CORS) {
        anyHost()
        allowHeader(HttpHeaders.ContentType)
    }

    install(CallLogging)

    routing {
        backendRouting()
        featureProviderRouting(httpClient, FeatureProviderRoutingConfig(fProviderHost, fProviderPort))
    }
}
