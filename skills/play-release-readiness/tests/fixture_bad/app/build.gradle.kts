plugins { id("com.android.application") }
android {
    compileSdk = 34
    defaultConfig {
        applicationId = "com.example.demo"
        minSdk = 24
        targetSdk = 34
        versionCode = 3
    }
    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}
dependencies {
    implementation("com.google.android.gms:play-services-ads:23.0.0")
    implementation("com.google.firebase:firebase-auth:22.0.0")
    implementation("com.google.firebase:firebase-analytics:21.0.0")
    implementation("com.google.ai.client.generativeai:generativeai:0.9.0")
}
