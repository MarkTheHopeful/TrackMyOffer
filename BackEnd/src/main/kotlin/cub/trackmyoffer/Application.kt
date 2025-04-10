package cub.trackmyoffer

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.cors.routing.*
import io.ktor.server.routing.*
import io.ktor.client.call.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.server.auth.*
import io.ktor.server.html.*
import io.ktor.server.response.*
import io.ktor.server.sessions.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.request.*
import kotlinx.html.*
import kotlinx.serialization.*
import kotlinx.serialization.json.Json

fun main(args: Array<String>) = EngineMain.main(args)

val applicationHttpClient = HttpClient(CIO) {
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true // Optional but recommended
        })
    }
}

fun Application.module() {
    val fProviderHost = environment.config.propertyOrNull("ktor.feature_provider.host")?.getString() ?: "0.0.0.0"
    val fProviderPort = environment.config.propertyOrNull("ktor.feature_provider.port")?.getString() ?: "8081"

    val httpClient = HttpClient(CIO) {
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

    install(Sessions) {
        cookie<UserSession>("user_session")
    }

    install(Authentication) {
        oauth("google-oauth") {
            client = applicationHttpClient
            providerLookup = {
                OAuthServerSettings.OAuth2ServerSettings(
                    name = "google",
                    authorizeUrl = "https://accounts.google.com/o/oauth2/auth",
                    accessTokenUrl = "https://accounts.google.com/o/oauth2/token",
                    requestMethod = HttpMethod.Post,
                    clientId = System.getenv("CLIENT_ID"),
                    clientSecret = System.getenv("CLIENT_SECRET"),
                    defaultScopes = listOf("profile", "email")
                )
            }
            urlProvider = { "http://localhost:8080/callback" }
        }
    }

    routing {
        backendRouting()
        authRouting(applicationHttpClient)
        featureProviderRouting(httpClient, FeatureProviderRoutingConfig(fProviderHost, fProviderPort))
    }
}
