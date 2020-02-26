<#function lookup p>
  <#if deployed?? >
      <#if deployed[p]?? >
          <#return deployed[p] />
      <#else>
          <#return deployed.container[p] />
      </#if>
  <#else>
      <#return container[p] />
  </#if>
</#function>

<#function scriptsPath>
    <#if deployed?? >
        <#return deployed.file.path />
    <#else>
        <#return previousDeployed.file.path />
    </#if>
</#function>
