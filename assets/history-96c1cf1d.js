import{_ as g,r as n,k as b,o as l,c as i,a as t,F as _,l as m,w,f as k,u as h,t as p,h as d,n as S,g as x,p as F,i as I,j as A}from"./bootstrap.min-c4c061eb.js";const D=a=>(F("data-v-f56046b4"),a=a(),I(),a),$=D(()=>t("div",{class:"title"},[t("h1",{class:"display-4"},"下载任务")],-1)),B={class:"centered-div"},C={class:"progress"},L=["onClick"],N={class:"alert alert-success"},V={__name:"App",setup(a){const r=n([]);let c=n(!1),u=n("");const y=async(e,o)=>{c.value=!1;try{const s=await d.get(`/api/down/del/${e}/`);c.value=!0,location.reload()}catch(s){console.error("Failed to fetch history data:",s)}},f=async()=>{try{const e=await d.get("/api/history/");r.value=e.data,v()}catch(e){console.error("Failed to fetch history data:",e)}},v=()=>{setInterval(async()=>{for(const e of r.value.history)if(e.percent!==100)try{const o=await d.get(`/api/history/${e.obid}/`);e.percent=o.data.percent}catch(o){console.error("Failed to fetch progress:",o)}},800)};return b(()=>{f()}),(e,o)=>(l(),i(_,null,[$,t("div",B,[(l(!0),i(_,null,m(r.value.history,s=>(l(),i("div",{key:s.obid,class:"history-item"},[t("h2",null,p(s.file_name),1),t("div",C,[t("div",{class:"progress-bar",style:S({width:`${s.percent}%`})},null,4)]),x(p(s.percent)+"% ",1),t("button",{class:"btn btn-danger mt-3",onClick:z=>y(s.obid,s.file_name)},"删除",8,L)]))),128)),w(t("div",N,[t("strong",null,p(h(u))+" 删除成功!",1)],512),[[k,h(c)]])])],64))}},j=g(V,[["__scopeId","data-v-f56046b4"]]);A(j).mount("#app");
