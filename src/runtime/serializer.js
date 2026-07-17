/** Serializer：迷你编排域模块。 */
export class Serializer {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createSerializer = (data={}) => new Serializer(data);
