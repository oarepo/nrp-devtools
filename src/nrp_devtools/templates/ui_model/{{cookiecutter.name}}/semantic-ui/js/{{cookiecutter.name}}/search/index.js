import {
  // parseSearchAppConfigs,
  createSearchAppsInit,
} from "@js/oarepo_ui/search";

/** NOTE: This reads configs for any search app present on a page
 *   In HTML/Jinja, a single search app instance is typically represented
 *   as a div with a config data attribute:
 *
 *   <div data-invenio-search-config='...' />
 */
// const [searchAppConfig, ...otherSearchAppConfigs] = parseSearchAppConfigs()

/** NOTE: To customize components in a specific search app instance,
 *   you need to obtain its `overridableIdPrefix` from the corresponding config first
 */
// const { overridableIdPrefix } = searchAppConfig

export const defaultComponentOverrides = {
  /** NOTE: Then you can then replace any existing search ui
   * component with your own implementation:
   *
   *  Following is a mapping where you can provide your own
   *  implementation of components identified by its overridableID:
   */
  // [`${overridableIdPrefix}.ActiveFilters.element`]: YourComponent,                // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ActiveFilters/ActiveFilters.js#L67-L85
  // [`${overridableIdPrefix}.AutocompleteSearchBar.element`]: YourComponent,       // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/AutocompleteSearchBar/AutocompleteSearchBar.js#L117-L140
  // [`${overridableIdPrefix}.BucketAggregation.element`]: YourComponent,           // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/BucketAggregation/BucketAggregation.js#L107-L120
  // [`${overridableIdPrefix}.BucketAggregationContainer.element`]: YourComponent,  // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/BucketAggregation/BucketAggregationValues.js#L111-L116
  // [`${overridableIdPrefix}.Count.Element`]: YourComponent,                       // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/Count/Count.js#L45-L47
  // [`${overridableIdPrefix}.EmptyResults.element`]: YourComponent,                // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/EmptyResults/EmptyResults.js#L77-L96
  // [`${overridableIdPrefix}.Error.element`]: YourComponent,                       // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/Error/Error.js#L39-L41
  // [`${overridableIdPrefix}.LayoutSwitcher.element`]: YourComponent,              // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/LayoutSwitcher/LayoutSwitcher.js#L57-L78
  // [`${overridableIdPrefix}.Pagination.element`]: YourComponent,                  // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/Pagination/Pagination.js#L116-L138
  // [`${overridableIdPrefix}.ResultsGrid.container`]: YourComponent,               // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ResultsGrid/ResultsGrid.js#L72-L78
  // [`${overridableIdPrefix}.ResultsGrid.item`]: YourComponent,                    // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ResultsGrid/ResultsGrid.js#L46-L54
  // [`${overridableIdPrefix}.ResultsList.container`]: YourComponent,               // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ResultsList/ResultsList.js#L66-L73
  // [`${overridableIdPrefix}.ResultsList.item`]: YourComponent,                    // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ResultsList/ResultsList.js#L40-L48
  // [`${overridableIdPrefix}.ResultsLoader.element`]: YourComponent,               // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ResultsLoader/ResultsLoader.js#L34-L36
  // [`${overridableIdPrefix}.ResultsMultiLayout.element`]: YourComponent,          // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ResultsMultiLayout/ResultsMultiLayout.js#L42-L51
  // [`${overridableIdPrefix}.ResultsPerPage.element`]: YourComponent,              // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/ResultsPerPage/ResultsPerPage.js#L91-L108
  // [`${overridableIdPrefix}.SearchApp.searchbar`]: YourComponent,                 // https://github.com/inveniosoftware/invenio-search-ui/blob/master/invenio_search_ui/assets/semantic-ui/js/invenio_search_ui/components/SearchBar.js#L22-L24
  // [`${overridableIdPrefix}.SearchApp.layout`]: YourComponent,                    // https://github.com/inveniosoftware/invenio-search-ui/blob/master/invenio_search_ui/assets/semantic-ui/js/invenio_search_ui/components/SearchApp.js#L85-L161
  // [`${overridableIdPrefix}.SearchApp.facets`]: YourComponent,                    // https://github.com/inveniosoftware/invenio-search-ui/blob/master/invenio_search_ui/assets/semantic-ui/js/invenio_search_ui/components/SearchAppFacets.js#L16-L26
  // [`${overridableIdPrefix}.SearchApp.results`]: YourComponent,                   // https://github.com/inveniosoftware/invenio-search-ui/blob/master/invenio_search_ui/assets/semantic-ui/js/invenio_search_ui/components/Results.js#L32-L55
  // [`${overridableIdPrefix}.SearchApp.resultsPane`]: YourComponent,               // https://github.com/inveniosoftware/invenio-search-ui/blob/master/invenio_search_ui/assets/semantic-ui/js/invenio_search_ui/components/SearchAppResultsPane.js#L24-L33
  // [`${overridableIdPrefix}.SearchApp.resultOptions`]: YourComponent,             // https://github.com/inveniosoftware/invenio-search-ui/blob/master/invenio_search_ui/assets/semantic-ui/js/invenio_search_ui/components/Results.js#L72-L113
  // [`${overridableIdPrefix}.SearchBar.element`]: YourComponent,                   // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/SearchBar/SearchBar.js#L141-L169
  // [`${overridableIdPrefix}.SearchHelpLinks`]: YourComponent,                     // https://github.com/inveniosoftware/invenio-search-ui/blob/master/invenio_search_ui/assets/semantic-ui/js/invenio_search_ui/components/common/facets.js#L67-L73
  // [`${overridableIdPrefix}.SearchFilters.Toggle.element`]: YourComponent,        // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/Toggle/Toggle.js#L35C1-L51C3
  // [`${overridableIdPrefix}.Sort.element`]: YourComponent,                        // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/Sort/Sort.js#L123-L140
  // [`${overridableIdPrefix}.SortBy.element`]: YourComponent,                      // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/SortBy/SortBy.js#L93-L110
  // [`${overridableIdPrefix}.SortOrder.element`]: YourComponent                    // https://github.com/inveniosoftware/react-searchkit/blob/master/src/lib/components/SortOrder/SortOrder.js#L95-L112
};

createSearchAppsInit({ defaultComponentOverrides });
