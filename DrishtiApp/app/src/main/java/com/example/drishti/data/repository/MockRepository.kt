package com.example.drishti.data.repository

import com.example.drishti.data.model.Announcement
import com.example.drishti.data.model.AnnouncementType
import com.example.drishti.data.model.Complaint
import com.example.drishti.data.model.ComplaintStatus
import com.example.drishti.data.model.User
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.UUID

object MockRepository {
    
    // Simulating logged-in user
    private val _currentUser = MutableStateFlow<User?>(
        User(
            id = "user_123",
            name = "Aditya Patil",
            email = "aditya@example.com",
            aadhaarNumber = "1234-5678-9012",
            karmaPoints = 850
        )
    )
    val currentUser: StateFlow<User?> = _currentUser.asStateFlow()

    // Simulating announcements
    private val _announcements = MutableStateFlow<List<Announcement>>(
        listOf(
            Announcement(
                id = UUID.randomUUID().toString(),
                title = "Water Supply Interruption",
                message = "Water supply will be interrupted in the downtown area tomorrow from 10 AM to 2 PM due to pipeline maintenance.",
                type = AnnouncementType.ALERT,
                timestamp = System.currentTimeMillis() - 3600000
            ),
            Announcement(
                id = UUID.randomUUID().toString(),
                title = "Community Townhall",
                message = "Join us this Friday for a townhall meeting to discuss the new park project.",
                type = AnnouncementType.EVENT,
                timestamp = System.currentTimeMillis() - 86400000
            )
        )
    )
    val announcements: StateFlow<List<Announcement>> = _announcements.asStateFlow()

    // Simulating complaints database
    private val _complaints = MutableStateFlow<List<Complaint>>(
        listOf(
            Complaint(
                id = UUID.randomUUID().toString(),
                title = "Pothole on Main Street",
                description = "Deep pothole causing traffic slowdowns and potential vehicle damage near the central park.",
                category = "Infrastructure",
                status = ComplaintStatus.PENDING,
                timestamp = System.currentTimeMillis() - 86400000 * 2, // 2 days ago
                authorId = "user_123",
                location = "Main Street, NY"
            ),
            Complaint(
                id = UUID.randomUUID().toString(),
                title = "Broken Streetlight",
                description = "Streetlight has been out for a week, making the neighborhood unsafe at night.",
                category = "Electrical",
                status = ComplaintStatus.IN_PROGRESS,
                timestamp = System.currentTimeMillis() - 86400000 * 5, // 5 days ago
                authorId = "user_123",
                location = "5th Avenue"
            ),
            Complaint(
                id = UUID.randomUUID().toString(),
                title = "Garbage Not Collected",
                description = "Trash bins are overflowing. It has been over a week since the last collection.",
                category = "Sanitation",
                status = ComplaintStatus.RESOLVED,
                timestamp = System.currentTimeMillis() - 86400000 * 10, // 10 days ago
                authorId = "user_123",
                location = "Elm Street Residential Area"
            )
        )
    )
    val complaints: StateFlow<List<Complaint>> = _complaints.asStateFlow()

    fun addComplaint(title: String, description: String, category: String, location: String) {
        val newComplaint = Complaint(
            id = UUID.randomUUID().toString(),
            title = title,
            description = description,
            category = category,
            status = ComplaintStatus.PENDING,
            timestamp = System.currentTimeMillis(),
            authorId = _currentUser.value?.id ?: "unknown",
            location = location
        )
        _complaints.value = listOf(newComplaint) + _complaints.value
    }
}
