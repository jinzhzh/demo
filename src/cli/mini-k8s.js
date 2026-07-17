#!/usr/bin/env node
import {MiniCluster} from '../runtime/cluster.js';
const c=new MiniCluster({storeFile:process.env.MINI_K8S_STATE}); const cmd=process.argv[2]||'demo';
if(cmd==='demo'){c.addNode('node-a',4000,8192,{zone:'a'});c.addNode('node-b',4000,8192,{zone:'b'});c.applyService({name:'web-svc',selector:{app:'web'},port:80});c.applyDeployment({name:'web',replicas:2,cpu:500,mem:512,minReplicas:2,maxReplicas:5,version:'v1'});c.scale('web',3);c.rollingUpdate('web','bad-v2');c.hpa('web',92,60);console.log('=== 集群状态 ===');console.log(JSON.stringify(c.status(),null,2));console.log('\n=== 事件时间线 ===');console.log(c.events.timeline())} else console.error('仅支持 demo 命令');
