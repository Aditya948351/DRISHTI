package com.example.drishti.data.model

data class User(
    val id: String,
    val name: String,
    val email: String,
    val aadhaarNumber: String,
    val profileImageUrl: String? = null,
    val karmaPoints: Int = 0
)