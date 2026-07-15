export function 渲染报告HTML({ 标本, 结果列表, 项目表 }) {
  const 行 = 结果列表.map(r => { const p = 项目表.find(x => x.id === r.项目ID); return `<tr><td>${p.名称}</td><td>${r.值}</td><td>${r.单位}</td><td>${p.参考区间}</td><td>${r.危急 ? '危急值' : '正常'}</td></tr>`; }).join('');
  return `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>检验报告</title><style>body{font-family:Arial,"Microsoft YaHei";margin:32px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #333;padding:8px;text-align:left}h1{text-align:center}</style><body><h1>华东示范医院检验报告单</h1><p>报告编号：RPT-${标本.id}　标本条码：${标本.条码}</p><p>患者：${标本.患者.姓名}　性别：${标本.患者.性别}　标本类型：${标本.标本类型}</p><table><thead><tr><th>项目</th><th>结果</th><th>单位</th><th>参考区间</th><th>标记</th></tr></thead><tbody>${行}</tbody></table><p>本报告仅供临床参考。</p></body></html>`;
}
