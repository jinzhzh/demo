/** Revision：迷你编排域模块。 */
export class Revision {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createRevision = (data={}) => new Revision(data);
