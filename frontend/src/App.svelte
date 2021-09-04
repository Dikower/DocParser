<script>
	import Router from "svelte-spa-router";
	import Landing from "./pages/landing.svelte";
	import Main from "./Pages/Main.svelte";
	
	const routes = {
		"/": Landing,
		"/main": Main,
	}
</script>

<Router {routes} />


