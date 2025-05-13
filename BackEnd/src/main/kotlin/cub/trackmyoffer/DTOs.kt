import kotlinx.serialization.*

@Serializable
data class EducationEntry(
    val id: Int,
    val institution: String,
    val degree: String,
    val startDate: String,    // ISO-8601 strings
    val endDate: String,
    val additionalInfo: String? = null
)

@Serializable
data class ProfileData(
    var id: Int? = null,
    @SerialName("first_name") val firstName: String,
    @SerialName("last_name")  val lastName: String,
    val email: String,
    val country: String? = null,
    val state: String? = null,
    val city: String? = null,
    @SerialName("linkedin_url")    val linkedinUrl: String? = null,
    @SerialName("github_url")      val githubUrl: String?   = null,
    @SerialName("personal_website")val personalWebsite: String? = null,
    @SerialName("other_url")       val otherUrl: String? = null,
    @SerialName("about_me")        val aboutMe: String? = null,
    val phone: String? = null,
    val education: List<EducationEntry> = emptyList(),
)