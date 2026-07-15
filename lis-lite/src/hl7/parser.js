export function 解析HL7(文本) {
  const 段 = Object.fromEntries(文本.trim().split(/\r?\n/).map(x => { const 字段 = x.split('|'); return [字段[0], 字段]; }));
  if (!段.MSH || !段.OBR || !段.OBX) throw new Error('HL7报文缺少MSH、OBR或OBX段');
  const obr = 段.OBR, obx = 段.OBX;
  return { 消息类型: 段.MSH[8], 消息ID: 段.MSH[9], 标本ID: obr[3], 项目ID: obx[3].split('^')[0], 结果值: Number(obx[5]), 单位: obx[6], 原始文本: 文本 };
}
export const 应答 = 消息ID => `MSH|^~\\&|LIS|HOSP-A|ANALYZER|HOSP-A|${new Date().toISOString()}||ACK|ACK-${消息ID}|P|2.5\nMSA|AA|${消息ID}`;
