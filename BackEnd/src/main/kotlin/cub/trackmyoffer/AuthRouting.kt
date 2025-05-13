package cub.trackmyoffer


import io.ktor.client.statement.*
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
import io.ktor.server.application.log

fun Route.authRouting(httpClient: HttpClient) {
    val vitePort = environment.config.propertyOrNull("ktor.frontend_vite.port")?.getString() ?: "5000"
    val viteHost = environment.config.propertyOrNull("ktor.frontend_vite.host")?.getString() ?: "localhost"
    val viteUrl = environment.config.propertyOrNull("ktor.frontend_vite.url")?.getString() ?: "http://$viteHost:$vitePort"

    authenticate("google-oauth") {
        get("/login") {
            application.log.info("Initiating Google OAuth login")
            // Redirect to Google OAuth
        }

        get("/callback") {
            val currentPrincipal: OAuthAccessTokenResponse.OAuth2? = call.authentication.principal()

            currentPrincipal?.let { principal ->
                principal.state?.let { state ->
                    call.sessions.set(UserSession(state, principal.accessToken))
                    call.respondRedirect("/home")
                    application.log.info("OAuth callback successful, session created")
                    return@get // Ensure no further response is sent
                }
            }

            application.log.warn("OAuth callback failed, redirecting to login")
            call.respondRedirect("/login")
        }
    }

    post("/logout") {
        application.log.info("Logout request received")
        val userSession: UserSession? = call.sessions.get()
        
        // Clear the session regardless of whether it exists
        call.sessions.clear<UserSession>()
        
        if (userSession != null) {
            application.log.info("Valid session found and cleared")
            call.respond(HttpStatusCode.OK, mapOf("status" to "success"))
        } else {
            application.log.info("No valid session found")
            call.respond(HttpStatusCode.OK, mapOf("status" to "already_logged_out"))
        }
    }

    get("/home") {
        val userSession: UserSession? = call.sessions.get()
        if (userSession != null && validateToken(httpClient, userSession)) {
            val userInfo: UserInfo = getUserInfo(httpClient, userSession)
            application.log.debug("User ${userInfo.email} redirected to frontend")
            call.respondRedirect(viteUrl)
        } else {
            application.log.debug("Invalid or expired session, redirecting to login")
            call.sessions.clear<UserSession>()
            call.respondRedirect("/login")
        }
    }

    get("/auth/status") {
        val userSession: UserSession? = call.sessions.get()
        if (userSession != null) {
            if (validateToken(httpClient, userSession)) {
                val userInfo: UserInfo = getUserInfo(httpClient, userSession)
                application.log.debug("Auth status check: authenticated for user ${userInfo.email}")
                call.respond(
                    AuthStatusResponse(
                        isAuthenticated = true,
                        userData = userInfo
                    )
                )
            } else {
                application.log.debug("Auth status check: token invalid or expired")
                call.sessions.clear<UserSession>()
                call.respond(
                    AuthStatusResponse(
                        isAuthenticated = false,
                        userData = null
                    )
                )
            }
        } else {
            application.log.debug("Auth status check: not authenticated")
            call.respond(
                AuthStatusResponse(
                    isAuthenticated = false,
                    userData = null
                )
            )
        }
    }
}

suspend fun validateToken(httpClient: HttpClient, userSession: UserSession): Boolean {
    return try {
        httpClient.get("https://oauth2.googleapis.com/tokeninfo") {
            url {
                parameters.append("access_token", userSession.token)
            }
        }.status == HttpStatusCode.OK
    } catch (e: Exception) {
        false
    }
}

suspend fun getUserInfo(
    httpClient: HttpClient,
    userSession: UserSession
): UserInfo = httpClient.get("https://www.googleapis.com/oauth2/v2/userinfo") {
    headers {
        append(HttpHeaders.Authorization, "Bearer ${userSession.token}")
    }
}.body()

private suspend fun getSession(
    call: ApplicationCall
): UserSession? {
    val userSession: UserSession? = call.sessions.get()
    //if there is no session, redirect to login
    if (userSession == null) {
        call.respondRedirect("/login")
        return null
    }
    return userSession
}

@Serializable
data class UserSession(val state: String, val token: String)

@Serializable
data class UserInfo(
    val id: String,
    val email: String,
    @SerialName("verified_email") val verifiedEmail: Boolean,
    val name: String,
    @SerialName("given_name") val givenName: String,
    @SerialName("family_name") val familyName: String,
    val picture: String
)

@Serializable
data class AuthStatusResponse(
    val isAuthenticated: Boolean,
    val userData: UserInfo?
)