/** FilterChain：迷你编排域模块。 */
export class FilterChain {
  constructor(data={}) { Object.assign(this, data) }
  snapshot() { return {...this} }
}
export const createFilterChain = (data={}) => new FilterChain(data);
