package cub.trackmyoffer

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.logging.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.auth.*
import io.ktor.server.netty.*
import io.ktor.server.plugins.calllogging.*
import io.ktor.server.plugins.cors.routing.*
import io.ktor.server.routing.*
import io.ktor.server.sessions.*
import kotlinx.serialization.json.Json
import kotlin.collections.listOf
import kotlin.collections.set
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation as ClientContentNegotiation
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation as ServerContentNegotiation

fun main(args: Array<String>) = EngineMain.main(args)

fun Application.module() {
    val oauthUrl = environment.config.propertyOrNull("ktor.oauth.url")?.getString() ?: "http://0.0.0.0:8080"
    val fProviderUrl = environment.config.propertyOrNull("ktor.feature_provider.url")?.getString() ?: "http://0.0.0.0:8081"

    val httpClient = HttpClient(CIO) {
        install(ClientContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true // Optional but recommended
            })
        }

        install(Logging) {
            logger = Logger.DEFAULT
            level = LogLevel.HEADERS
        }

        expectSuccess = false
        engine {
            requestTimeout = 10_000
        }
    }

    val utilityDatabase = UtilityDatabase(httpClient, fProviderUrl)
    utilityDatabase.init()

    install(CORS) {
        anyHost()
        allowCredentials = true
        allowMethod(HttpMethod.Get)
        allowMethod(HttpMethod.Delete)
        allowMethod(HttpMethod.Post)
        allowMethod(HttpMethod.Options)  // Important for preflight requests
        allowHeader(HttpHeaders.ContentType)
        allowHeader(HttpHeaders.Authorization)
        allowHeader(HttpHeaders.Accept)
        exposeHeader(HttpHeaders.ContentType)
        exposeHeader(HttpHeaders.Authorization)
    }

    install(CallLogging)
    install(Sessions) {
        cookie<UserSession>("user_session") {
            cookie.path = "/"
            cookie.secure = true
            cookie.httpOnly = true
            cookie.extensions["SameSite"] = "None"

            val domain = System.getenv("COOKIE_DOMAIN")
            if (!domain.isNullOrEmpty()) {
                cookie.domain = domain
            }
            cookie.maxAgeInSeconds = 3600 // Set an appropriate timeout (e.g., 1 hour)
        }
    }

    install(ServerContentNegotiation) {
        json()
    }

    install(Authentication) {
        oauth("google-oauth") {
            client = httpClient
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
            urlProvider = { "$oauthUrl/callback" }
        }
    }

    routing {
        backendRouting()
        authRouting(httpClient)
        featureProviderRouting(httpClient, FeatureProviderRoutingConfig(fProviderUrl), utilityDatabase)
        userRouting(httpClient, utilityDatabase)
    }
}
