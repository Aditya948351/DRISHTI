package com.example.drishti.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.drishti.ui.screens.DashboardScreen
import com.example.drishti.ui.screens.ReportIssueScreen
import com.example.drishti.ui.screens.TrackingScreen

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "dashboard") {
        composable("dashboard") {
            DashboardScreen(navController)
        }
        composable("report_issue") {
            ReportIssueScreen(navController)
        }
        composable("tracking") {
            TrackingScreen(navController)
        }
    }
}
