/** Namespace：迷你编排域模块。 */
export class Namespace {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createNamespace = (data={}) => new Namespace(data);
