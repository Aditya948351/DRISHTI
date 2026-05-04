package com.example.drishti.data.model

data class Announcement(
    val id: String,
    val title: String,
    val message: String,
    val type: AnnouncementType,
    val timestamp: Long
)

enum class AnnouncementType(val displayName: String) {
    ALERT("Alert"),
    INFO("Info"),
    EVENT("Event")
}
