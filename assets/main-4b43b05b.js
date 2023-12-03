import{_ as A,r as a,o as B,a as r,c as u,b as e,t as D,w as d,v as I,d as O,e as V,f as g,g as R,u as b,h as p,F as S,i as P,p as q,j as C,k as N}from"./bootstrap.min-045aca3c.js";import{a as L}from"./axios-47b9d439.js";const j="/assets/setting.png";const l=v=>(q("data-v-e2d53917"),v=v(),C(),v),E=l(()=>e("img",{src:j,alt:"Your Image",class:"img-fluid",style:{width:"30px",height:"30px"},"data-bs-toggle":"modal","data-bs-target":"#settingModal"},null,-1)),K={class:"modal fade",id:"settingModal",tabindex:"-1","aria-labelledby":"exampleModalLabel","aria-hidden":"true"},W={class:"modal-dialog"},X={class:"modal-content"},Y=l(()=>e("div",{class:"modal-header"},[e("h5",{class:"modal-title",id:"exampleModalLabel"},"设置"),e("button",{type:"button",class:"btn-close","data-bs-dismiss":"modal","aria-label":"Close"})],-1)),z={class:"modal-body"},G=l(()=>e("p",null,[p("您使用本软件即代表您同意最终用户许可协议("),e("a",{href:"/eula"},"此处"),p(")")],-1)),H=l(()=>e("p",null,"© 2022-2023 FlyStudioKey. All Rights Reserved.",-1)),J=l(()=>e("div",{class:"modal-footer"},[e("button",{type:"button",class:"btn btn-danger","data-bs-dismiss":"modal"},"关闭")],-1)),Q={key:0,class:"container d-flex justify-content-center align-items-center centered-div"},Z={class:"text-center"},$=l(()=>e("h1",{class:"display-4"},"番茄小说下载器",-1)),ee={class:"form-check form-check-inline"},te=l(()=>e("label",{class:"form-check-label",for:"singleDownload"},"单文件下载",-1)),le={class:"form-check form-check-inline"},oe=l(()=>e("label",{class:"form-check-label",for:"bulkDownload"},"批量下载",-1)),se={class:"mt-3"},ae=l(()=>e("label",{for:"formatOption"},"文件格式：",-1)),ne=l(()=>e("option",{value:"txt"},"TXT(普通文档)",-1)),ie=l(()=>e("option",{value:"epub"},"EPUB(电子书)",-1)),de=[ne,ie],re={key:0,class:"mt-3 url-box"},ue=l(()=>e("label",{for:"urlInput"},"URL：",-1)),ce={key:1,class:"mt-3 url-box"},_e=l(()=>e("label",{for:"bulkUrlInput"},"URL（每行一个）：",-1)),pe=l(()=>e("br",null,null,-1)),ve=l(()=>e("br",null,null,-1)),he={class:"alert alert-success"},me=l(()=>e("strong",null,"成功!",-1)),fe={class:"alert alert-warning"},ge=l(()=>e("strong",null,"警告!",-1)),be={class:"alert alert-warning"},ye=l(()=>e("strong",null,"警告!",-1)),we=l(()=>e("button",{class:"btn btn-primary mt-3"},[e("a",{href:"/history",style:{"text-decoration":"none",color:"inherit"}},"下载任务")],-1)),ke={__name:"App",setup(v){const M=a(!0);let h=a(!1),m=a(!1),f=a(!1);a(!0);let y=a([]);a([]);const n=a("single"),i=a(""),w=a(""),c=a("epub"),k=a("");document.title="番茄小说下载器";let _=[];const T=async()=>{if(h.value=!1,m.value=!1,f.value=!1,n.value==="single")if(console.log("Downloading single file:",i.value),x(i.value)&&(i.value.includes("/page/")||i.value.includes("&book_id="))){console.log("Downloading single file:",i.value);let s=await U([i.value],c.value);s.data.return.length>0?(y.value=s.data.return,f.value=!0):h.value=!0}else m.value=!0;else if(n.value==="bulk")if(_=w.value.split(`
`),console.log("Downloading multiple files:",_),_.every(t=>x(t)&&(t.includes("/page/")||t.includes("&book_id=")))){console.log("Downloading multiple files:",_);let t=await U(_,c.value);t.data.return.length>0?(y.value=t.data.return,f.value=!0):h.value=!0}else m.value=!0};function x(s){return/^https?:\/\/.+/.test(s)}async function U(s,t){try{const o=await L.post("/api/down/",{urls:s,format:t});return console.log("POST request successful:",o.data),o}catch(o){console.error("POST request failed:",o)}}const F=async()=>{try{const s=await L.get("/api/get_config/");console.log(s.data),c.value=s.data.default_download_mode,k.value=s.data.version,console.log("Fetched config:",k.value)}catch(s){console.error("Failed to fetch history data:",s)}};return B(()=>{F()}),(s,t)=>(r(),u(S,null,[E,e("div",K,[e("div",W,[e("div",X,[Y,e("div",z,[e("p",null,"当前版本： "+D(k.value),1),G,H]),J])])]),M.value?(r(),u("div",Q,[e("div",Z,[$,e("div",ee,[d(e("input",{class:"form-check-input",type:"radio",name:"downloadType",id:"singleDownload",value:"single","onUpdate:modelValue":t[0]||(t[0]=o=>n.value=o)},null,512),[[I,n.value]]),te]),e("div",le,[d(e("input",{class:"form-check-input",type:"radio",name:"downloadType",id:"bulkDownload",value:"bulk","onUpdate:modelValue":t[1]||(t[1]=o=>n.value=o)},null,512),[[I,n.value]]),oe]),e("div",se,[ae,d(e("select",{class:"form-control",id:"formatOption","onUpdate:modelValue":t[2]||(t[2]=o=>c.value=o)},de,512),[[O,c.value]])]),n.value==="single"?(r(),u("div",re,[ue,d(e("input",{type:"text",class:"form-control",id:"urlInput","onUpdate:modelValue":t[3]||(t[3]=o=>i.value=o),placeholder:"输入URL"},null,512),[[V,i.value]])])):g("",!0),n.value==="bulk"?(r(),u("div",ce,[_e,d(e("textarea",{class:"form-control",id:"bulkUrlInput",rows:"5","onUpdate:modelValue":t[4]||(t[4]=o=>w.value=o),placeholder:"输入多个URL，每行一个"},null,512),[[V,w.value]])])):g("",!0),e("button",{class:"btn btn-primary mt-3",onClick:T},"提交"),pe,ve,d(e("div",he,[me,p(" 加入下载列表！ ")],512),[[R,b(h)]]),d(e("div",fe,[ge,p(" 请输入正确的目录链接！ ")],512),[[R,b(m)]]),b(f)?(r(!0),u(S,{key:2},P(b(y),o=>(r(),u("div",be,[ye,p(" "+D(o)+" 重复提交 ",1)]))),256)):g("",!0)]),we])):g("",!0)],64))}},xe=A(ke,[["__scopeId","data-v-e2d53917"]]);N(xe).mount("#app");