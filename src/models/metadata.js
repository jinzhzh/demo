/** Metadata：迷你编排域模块。 */
export class Metadata {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createMetadata = (data={}) => new Metadata(data);
