/** ResourceRequest：迷你编排域模块。 */
export class ResourceRequest {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createResourceRequest = (data={}) => new ResourceRequest(data);
