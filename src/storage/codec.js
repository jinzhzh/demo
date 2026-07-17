/** Codec：迷你编排域模块。 */
export class Codec {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createCodec = (data={}) => new Codec(data);
