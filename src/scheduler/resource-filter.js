/** ResourceFilter：迷你编排域模块。 */
export class ResourceFilter {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createResourceFilter = (data={}) => new ResourceFilter(data);
