/** PortMap：迷你编排域模块。 */
export class PortMap {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createPortMap = (data={}) => new PortMap(data);
