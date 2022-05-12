<template>
  <div class="searchbar-container">
    <!-- <a-input-search
      v-model:value="value"
      class="searchbar"
      size="large"
      placeholder="Bijvoorbeeld 'kerst' of 'CTR'"
      enter-button="Zoeken"
      allow-clear
      :bordered="false"
      @search="onSearch"
    >
      <template #prefix>
        <search-outlined />
      </template>
    </a-input-search> -->
    <ais-instant-search :search-client="searchClient" index-name="experiments">
      <ais-configure :hits-per-page.camel="8" />
      <div class="search-panel">
        <div class="search-panel__filters">
          <h4 class="mt-2">Klanttype</h4>
          <ais-refinement-list attribute="Klanttype" />
          <h4 class="mt-2">Apparaatcategorie</h4>
          <ais-refinement-list attribute="Apparaatcategorie" />
          <h4 class="mt-2">Funnel</h4>
          <ais-refinement-list attribute="Funnel" />
        </div>
        <div class="search-panel__results">
          <div class="searchbox">
            <ais-search-box />
          </div>
          <ais-hits>
            <template #item="{ item }">
              <div class="hit-title">{{ item.Titel }}</div>
            </template>
          </ais-hits>
        </div>
      </div>
    </ais-instant-search>
  </div>
</template>
<script>
import TypesenseInstantSearchAdapter from "typesense-instantsearch-adapter";
// import { AisInstantSearch, AisSearchBox,  } from "vue-instantsearch/vue3/es";

const typesenseInstantsearchAdapter = new TypesenseInstantSearchAdapter({
  server: {
    apiKey: "AAAA", // Be sure to use an API key that only allows search operations
    nodes: [
      {
        host: "35.204.119.30",
        port: "8108",
        protocol: "http",
      },
    ],
    cacheSearchResultsForSeconds: 2 * 60, // Cache search results from server. Defaults to 2 minutes. Set to 0 to disable caching.
  },
  // The following parameters are directly passed to Typesense's search API endpoint.
  //  So you can pass any parameters supported by the search endpoint below.
  //  query_by is required.
  additionalSearchParameters: {
    query_by: "Titel,Actie,Situatie", // Wat kunnen andere hiermee?
  },
});
const searchClient = typesenseInstantsearchAdapter.searchClient;

export default {
  // components: {
  //   AisInstantSearch,
  //   AisSearchBox,
  // },
  data() {
    return {
      searchClient,
    };
  },
};
</script>

<style lang="scss">
.searchbar-container {
  background: #fff;
}
.searchbar .ant-input-affix-wrapper {
  height: 72px;
}

.searchbar .ant-btn {
  height: 72px !important;
  //   background-color: #fad981;
  //   color: #262626;
}

.searchbar .ant-input-affix-wrapper-borderless,
.ant-input-affix-wrapper-borderless,
.ant-input-affix-wrapper-borderless:hover,
.ant-input-affix-wrapper-borderless:focus,
.ant-input-affix-wrapper-borderless-focused {
  background: #fff;
}

.header {
  display: flex;
  align-items: center;
  min-height: 50px;
  padding: 0.5rem 1rem;
  background-image: linear-gradient(to right, #4dba87, #2f9088);
  color: #fff;
  margin-bottom: 1rem;
}
.header a {
  color: #fff;
  text-decoration: none;
}
.header-title {
  font-size: 1.2rem;
  font-weight: normal;
}
.header-title::after {
  content: " ▸ ";
  padding: 0 0.5rem;
}
.header-subtitle {
  font-size: 1.2rem;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}
.search-panel {
  display: flex;
}
.search-panel__filters {
  flex: 1;
}
.search-panel__results {
  flex: 3;
}
.ais-Highlight-highlighted {
  color: inherit;
  font-size: inherit;
}
.searchbox {
  margin-bottom: 2rem;
}
.pagination {
  margin: 2rem auto;
  text-align: center;
}
.hit-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin-top: 10px;
}
.hit-authors {
  margin-top: 3px;
  font-size: 0.8rem;
}
.hit-publication-year {
  font-size: 0.8rem;
  margin-top: 20px;
}
.hit-rating {
  margin-top: 3px;
  font-size: 0.8rem;
}
.ais-Hits-item {
  padding: 30px;
  box-shadow: none;
  border: 1px solid lighten(lightgray, 8%);
}
</style>
