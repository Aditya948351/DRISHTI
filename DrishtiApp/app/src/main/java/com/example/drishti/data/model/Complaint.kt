package com.example.drishti.data.model

data class Complaint(
    val id: String,
    val title: String,
    val description: String,
    val category: String,
    val status: ComplaintStatus,
    val timestamp: Long,
    val authorId: String,
    val location: String? = null,
    val imageUrl: String? = null
)

enum class ComplaintStatus(val displayName: String) {
    PENDING("Pending"),
    IN_PROGRESS("In Progress"),
    RESOLVED("Resolved"),
    REJECTED("Rejected")
}
