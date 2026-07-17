/** Binding：迷你编排域模块。 */
export class Binding {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createBinding = (data={}) => new Binding(data);
