<script>
	import Router from "svelte-spa-router";

	import Landing from "./pages/landing.svelte";
	import Authorization from "./Pages/Authorization.svelte";
	import BankPage from "./Pages/BankPage.svelte";
	import CompanyPage from "./Pages/CompanyPage.svelte";
	
	const routes = {
		"/": Landing,
		"/auth": Authorization,
		"/comp": CompanyPage,
		"/bank": BankPage,
	}
</script>

<Router {routes} />


