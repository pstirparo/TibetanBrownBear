<template>
  <div>
    Graph
    <table class='table'>
      <tr><th>Link name</th><th>Object</th></tr>
      <tr v-for="edge in graph.edges"
          v-bind:key='edge._id'>
        <td>{{edge.relationship_type}}</td><td>{{getVerticeForEdge(graph, edge)}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios'
import TableFilter from '@/components/scaffolding/TableFilter'

export default {
  components: {
    TableFilter
  },
  props: ['object'],
  data () {
    return {
      graph: []
    }
  },
  computed: {
    apiPath () {
      return 'http://localhost:5000/api/entities/' + this.object.id + '/neighbors'
    }
  },
  methods: {
    fetchNeighbors () {
      console.log('fetching neighbors for ' + this.object.id)
      axios.get(this.apiPath)
        .then(response => {
          console.log('Got ' + response.data.edges.length + ' edges')
          this.graph = response.data
        })
    },
    getVerticeForEdge (graph, edge) {
      if (edge.source_ref === this.object.id) {
        return graph.vertices[edge.target_ref].name
      }
      return graph.vertices[edge.source_ref].name
    }
  },
  watch: {
    object: 'fetchNeighbors'
  }
}
</script>
