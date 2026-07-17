/** Watch：迷你编排域模块。 */
export class Watch {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createWatch = (data={}) => new Watch(data);
