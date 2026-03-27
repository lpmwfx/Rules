---
tags: [uiux, menus, android, compose, material3, bottom-nav]
concepts: [native-menus, android-navigation, material-design, bottom-navigation]
related: [uiux/help-about.md, uiux/state-flow.md]
keywords: [android, compose, bottom-nav, navigationbar, overflow-menu, top-app-bar, material3, three-dot, drawersheet]
layer: 4
---
# Android Navigation — Kotlin + Jetpack Compose

> No menubar on Android — Bottom Navigation + Top App Bar overflow menu

---

VITAL: Android has no menubar — use BottomNavigation for primary nav, overflow menu for secondary actions
VITAL: Bottom Navigation max 5 items — use Navigation Drawer if more destinations are needed
RULE: Top App Bar overflow menu (three-dot) contains: Settings, Help, About, Report Issue
RULE: Settings opens a dedicated Settings screen via NavController — not a dialog
RULE: About is a full-screen composable or AlertDialog
RULE: Back navigation is handled by the system — do NOT add explicit back buttons to top-level screens
RULE: Use NavController + NavHost for all navigation — no manual Fragment transactions
BANNED: Traditional menubar widget on Android
BANNED: BottomNavigationBar with more than 5 items
BANNED: Mixing Fragment transactions with NavController
BANNED: Opening Settings as a Dialog — it must be a full screen

## Android Navigation Structure

```
Top App Bar
┌──────────────────────────────────────────┐
│  ←  MyApp                           [⋮]  │   ← overflow: Settings, Help, About
└──────────────────────────────────────────┘
       (content area)
┌──────────────────────────────────────────┐
│  [Home]  [Search]  [Library]  [Profile]  │   ← BottomNavigationBar (max 5)
└──────────────────────────────────────────┘
```

Overflow menu (three-dot):
```
Settings
Help
Report Issue
─────────
About MyApp
```

## Compose Implementation

```kotlin
// Navigation graph
@Composable
fun AppNavGraph(navController: NavHostController) {
    NavHost(navController = navController, startDestination = "home") {
        composable("home")     { HomeScreen(navController) }
        composable("search")   { SearchScreen(navController) }
        composable("library")  { LibraryScreen(navController) }
        composable("settings") { SettingsScreen(navController) }
        composable("about")    { AboutScreen(navController) }
    }
}
```

```kotlin
// Top App Bar with overflow
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppTopBar(
    title: String,
    navController: NavHostController,
) {
    var showMenu by remember { mutableStateOf(false) }

    TopAppBar(
        title = { Text(title) },
        actions = {
            IconButton(onClick = { showMenu = true }) {
                Icon(Icons.Default.MoreVert, contentDescription = "More options")
            }
            DropdownMenu(expanded = showMenu, onDismissRequest = { showMenu = false }) {
                DropdownMenuItem(
                    text = { Text("Settings") },
                    onClick = { showMenu = false; navController.navigate("settings") },
                    leadingIcon = { Icon(Icons.Default.Settings, null) }
                )
                DropdownMenuItem(
                    text = { Text("Help") },
                    onClick = { showMenu = false; navController.navigate("help") },
                    leadingIcon = { Icon(Icons.Default.Help, null) }
                )
                DropdownMenuItem(
                    text = { Text("Report Issue") },
                    onClick = { showMenu = false; /* open browser or issue screen */ },
                )
                HorizontalDivider()
                DropdownMenuItem(
                    text = { Text("About") },
                    onClick = { showMenu = false; navController.navigate("about") },
                )
            }
        }
    )
}
```

```kotlin
// Bottom navigation
@Composable
fun AppBottomBar(navController: NavHostController) {
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    NavigationBar {
        listOf(
            Triple("home",    Icons.Default.Home,    "Home"),
            Triple("search",  Icons.Default.Search,  "Search"),
            Triple("library", Icons.Default.Book,    "Library"),
            Triple("profile", Icons.Default.Person,  "Profile"),
        ).forEach { (route, icon, label) ->
            NavigationBarItem(
                icon = { Icon(icon, contentDescription = label) },
                label = { Text(label) },
                selected = currentRoute == route,
                onClick = {
                    navController.navigate(route) {
                        popUpTo(navController.graph.startDestinationId) { saveState = true }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}
```

## Navigation Drawer (>5 destinations)

Use `ModalNavigationDrawer` when more than 5 top-level destinations exist:

```kotlin
ModalNavigationDrawer(
    drawerContent = {
        ModalDrawerSheet {
            Spacer(Modifier.height(12.dp))
            destinations.forEach { item ->
                NavigationDrawerItem(
                    label = { Text(item.label) },
                    selected = currentRoute == item.route,
                    icon = { Icon(item.icon, null) },
                    onClick = { navController.navigate(item.route); closeDrawer() }
                )
            }
        }
    }
) { /* content */ }
```

RULE: Switch to NavigationDrawer when destination count exceeds 5 — do not squeeze BottomNav

## About Screen

```kotlin
@Composable
fun AboutScreen(navController: NavHostController) {
    val uriHandler = LocalUriHandler.current

    Scaffold(topBar = { TopAppBar(title = { Text("About") },
        navigationIcon = { IconButton(onClick = { navController.popBackStack() }) {
            Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
        }}) }
    ) { padding ->
        Column(
            Modifier.padding(padding).padding(24.dp).fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            Image(painterResource(R.drawable.ic_launcher), null, Modifier.size(72.dp))
            Text(stringResource(R.string.app_name), style = MaterialTheme.typography.headlineMedium)
            Text(BuildConfig.VERSION_NAME, style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(stringResource(R.string.app_description), textAlign = TextAlign.Center)
            OutlinedButton(onClick = { uriHandler.openUri("https://yoursite.example") }) {
                Text("yoursite.example")
            }
            TextButton(onClick = { uriHandler.openUri("https://yoursite.example/license") }) {
                Text("GPL-3.0 License")
            }
        }
    }
}
```

RULE: About screen shows: app icon, name, version, description, website link, license link
RULE: Website and license are tappable — not plain text


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
