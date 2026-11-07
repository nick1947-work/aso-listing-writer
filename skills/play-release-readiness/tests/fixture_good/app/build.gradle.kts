plugins { id("com.android.application") }
android {
    compileSdk { version = release(36) }
    defaultConfig { applicationId = "in.creationunicorn.notes"; minSdk = 26; targetSdk = 36; versionCode = 10 }
    buildTypes { release { isMinifyEnabled = true } }
}
dependencies { implementation("androidx.room:room-runtime:2.7.0") }
