package cub.trackmyoffer

import io.ktor.client.*
import io.ktor.server.application.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import io.ktor.server.sessions.*

suspend fun Route.extractUserId(
    call: RoutingCall,
    httpClient: HttpClient,
    utilityDatabase: UtilityDatabase
): Int {
    val userSession: UserSession =
        call.sessions.get() ?: throw RuntimeException("Invalid session during request")

    if (!validateToken(httpClient, userSession)) {
        application.log.debug("Invalid or expired session, redirecting to login")
        call.sessions.clear<UserSession>()
        call.respondRedirect("/login")
    }
    val userInfo: UserInfo = getUserInfo(httpClient, userSession)

    // Get or create profile ID from the utility database
    return utilityDatabase.getOrCreateProfileId(userInfo.email, userInfo)
}
