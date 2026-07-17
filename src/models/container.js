/** Container：迷你编排域模块。 */
export class Container {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createContainer = (data={}) => new Container(data);
