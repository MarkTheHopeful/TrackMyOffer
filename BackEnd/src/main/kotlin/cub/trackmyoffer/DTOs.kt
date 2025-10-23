import kotlinx.serialization.*

@Serializable
data class EducationEntry(
    var id: Int? = null,
    val institution: String,
    val degree: String,
    @SerialName("start_date") val startDate: String,    // ISO-8601 strings
    @SerialName("end_date") val endDate: String? = null,
    @SerialName("additional_info") val additionalInfo: String? = null
)

@Serializable
data class ProfileData(
    var id: Int? = null,
    @SerialName("first_name") val firstName: String,
    @SerialName("last_name") val lastName: String,
    val email: String,
    val country: String? = null,
    val state: String? = null,
    val city: String? = null,
    @SerialName("linkedin_url") val linkedinUrl: String? = null,
    @SerialName("github_url") val githubUrl: String? = null,
    @SerialName("personal_website") val personalWebsite: String? = null,
    @SerialName("other_url") val otherUrl: String? = null,
    @SerialName("about_me") val aboutMe: String? = null,
    val phone: String? = null,
)

@Serializable
data class ExperienceEntry(
    var id: Int? = null,
    @SerialName("profile_id") var profileId: Int? = null,
    @SerialName("job_title") val jobTitle: String,
    val company: String,
    @SerialName("start_date") val startDate: String,    // ISO-8601 strings
    @SerialName("end_date") val endDate: String? = null,
    val description: String? = null,
)

@Serializable
data class WithJobDescription(
    val jobDescription: String,
)

@Serializable
data class CoverLetterRequest(
    val jobDescription: String,
    val motivations: String,
    val tone: String,
)

@Serializable
data class AchievementRewriteRequest(
    val achievementText: String,
    val style: String? = null,
    val context: String? = null,
)

@Serializable
data class AchievementRewriteResponse(
    @SerialName("original_achievement") val originalAchievement: String,
    @SerialName("rewritten_achievement") val rewrittenAchievement: String,
    val style: String,
)

@Serializable
data class AchievementsRewriteRequest(
    val achievements: List<String>,
    val style: String? = null,
    val context: String? = null,
)

@Serializable
data class AchievementsRewriteItem(
    @SerialName("original_achievement") val originalAchievement: String,
    @SerialName("rewritten_achievement") val rewrittenAchievement: String,
    val style: String,
)

@Serializable
data class AchievementsRewriteResponse(
    val results: List<AchievementsRewriteItem>
)
