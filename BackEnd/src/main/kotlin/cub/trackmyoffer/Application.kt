package cub.trackmyoffer

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.cors.routing.*
import io.ktor.server.routing.*
import io.ktor.client.call.*
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation as ClientContentNegotiation
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation as ServerContentNegotiation
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
    install(ClientContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true // Optional but recommended
        })
    }
}

fun Application.module() {
    val oauthtHost = environment.config.propertyOrNull("ktor.oauth.host")?.getString() ?: "localhost"
    val oauthPort = environment.config.propertyOrNull("ktor.oauth.port")?.getString() ?: "8080"
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
        allowHost("localhost:5000", schemes = listOf("http"))
        allowHost("localhost:8080", schemes = listOf("http"))
        allowCredentials = true
        allowMethod(HttpMethod.Get)
        allowMethod(HttpMethod.Post)
        allowMethod(HttpMethod.Options)  // Important for preflight requests
        allowHeader(HttpHeaders.ContentType)
        allowHeader(HttpHeaders.Authorization)
        allowHeader(HttpHeaders.Accept)
        exposeHeader(HttpHeaders.ContentType)
        exposeHeader(HttpHeaders.Authorization)
    }

    install(Sessions) {
        cookie<UserSession>("user_session") {
            cookie.path = "/"
            cookie.secure = false // Set to true in production
        }
    }

    install(ServerContentNegotiation) {
        json()
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
            urlProvider = { "http://$oauthtHost:$oauthPort/callback" }
        }
    }

    routing {
        backendRouting()
        authRouting(applicationHttpClient)
        featureProviderRouting(httpClient, FeatureProviderRoutingConfig(fProviderHost, fProviderPort))
    }
}
