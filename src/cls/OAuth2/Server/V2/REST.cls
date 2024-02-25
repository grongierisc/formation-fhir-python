Class OAuth2.Server.V2.REST Extends OAuth2.Server.REST
{

ClassMethod OnPreDispatch(
	pUrl As %String,
	pMethod As %String,
	ByRef pContinue As %Boolean) As %Status
{
    // Remove scope to force the use of the default scope
    set %request.Data("scope",1) = ""
    Quit $$$OK
}

}
