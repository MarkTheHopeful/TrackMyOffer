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

fun Route.authRouting(httpClient: HttpClient) {
    val vitePort = environment.config.propertyOrNull("ktor.frontend_vite.port")?.getString() ?: "5000"
    val viteHost = environment.config.propertyOrNull("ktor.frontend_vite.host")?.getString() ?: "localhost"

    authenticate("google-oauth") {
        get("/login") {
            // Redirect to Google OAuth
        }

        get("/callback") {
            val currentPrincipal: OAuthAccessTokenResponse.OAuth2? = call.authentication.principal()

            currentPrincipal?.let { principal ->
                principal.state?.let { state ->
                    call.sessions.set(UserSession(state, principal.accessToken))
                    call.respondRedirect("/home")
                    return@get // Ensure no further response is sent
                }
            }

            call.respondRedirect("/login")
        }
    }

    get("/home") {
        val userSession: UserSession? = getSession(call)
        if (userSession != null) {
            val userInfo: UserInfo = getPersonalGreeting(httpClient, userSession)
            call.respondRedirect("http://$viteHost:$vitePort/")
        }
    }

    get("/logout") {
        call.sessions.clear<UserSession>()
        call.respondRedirect("/login")
    }
}

private suspend fun getPersonalGreeting(
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
