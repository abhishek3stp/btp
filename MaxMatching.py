class MaxMatching(object):
    def __init__(self, V):
        # Initialize the MaxMatching object with member variables like LABEL,
        # MATE, FIRST, END, adjacency list graph, outerEdges, outerVertices

        self.V = V
        VPlusOne = V+1
        self.VPlusOne = VPlusOne
        self.END = list()
        self.graph = [list() for _ in range(VPlusOne)]

        self.outerEdges = list()
        self.outerVertices = set()
        self.outerIdx = 0

        # E0 init
        self.LABEL = [-1] * VPlusOne
        self.MATE = [0] * VPlusOne
        self.FIRST = [0] * VPlusOne

    def addEdge(self, v, w):
        # Adds vertices to END array and updates adjacency list with the
        # corresponding edge number n(vw)

        n_vw = len(self.END) + self.VPlusOne
        self.END.append(v)
        self.END.append(w)

        self.graph[v].append(n_vw)
        self.graph[w].append(n_vw)

    def getEdge(self, n_vw):
        # Gets the tuple corresponding to edge number n(vw)

        n_vw -= self.VPlusOne
        return (self.END[n_vw], self.END[n_vw+1])

    def getMatchingSize(self):
        # Gets the size of current matching i.e. |M|. After algorithm E has run,
        # the return value will correspond to maximum matching of graph

        return sum(map(lambda x: 1 if x > 0 else 0, self.MATE[1:]))

    def setLabel(self, v, label):
        # Updates the LABEL array for the object and updates outerVertices and
        # outerEdges if the new label is an outer label

        self.LABEL[v] = label

        if label >= 0 and v not in self.outerVertices:
            self.outerVertices.add(v)
            self.outerEdges.extend([(v, e) for e in self.graph[v]])

    def hasVertexLabel(self, v):
        # Check whether the vertex has a vertex label

        return self.LABEL[v] >= 1 and self.LABEL[v] <= self.V

    def hasEdgeLabel(self, v):
        # Check whether the vertex has an edge label

        WTimesTwo = len(self.END)
        return self.LABEL[v] > self.V and self.LABEL <= self.V + WTimesTwo

    def hasStartLabel(self, v):
        # Check whether the vertex has a start label

        return self.LABEL[v] == 0

    def chooseAnEdge(self):
        # Choose an outer edge xy where x is outer using the "breadth-first"
        # method suggested by the paper
        
        # E2
        if len(self.outerEdges) > self.outerIdx:
            x_nxy = self.outerEdges[self.outerIdx]
            self.outerIdx += 1
            return x_nxy
        return None, None

    def stopTheSearch(self):
        # Performs the step E7 in the algorithm that makes all vertices nonouter
        # for the next search

        # E7
        self.LABEL[0] = -1
        for v in self.outerVertices:
            self.setLabel(v, -1)
            self.setLabel(self.MATE[v], -1)
        self.outerVertices.clear()
        self.outerEdges.clear()
        self.outerIdx = 0

    def isMatched(self, v):
        # Check if a vertex v is matched by the algorithm yet

        return self.MATE[v] > 0

    def isOuterVertex(self, v):
        # Check if a vertex v is labelled as an outer vertex by the algorithm yet

        return v in self.outerVertices

    def setFlag(self, v, n_xy):
        # Flags vertex v with edge number n_xy

        self.setLabel(v, -n_xy)

    def isFlagged(self, v, n_xy):
        # Check if a vertex v is flagged with an edge by L

        return self.LABEL[v] == -n_xy

    def L(self, x, y, n_xy):
        # L assigns the edge label n(xy) to nonouter vertices. Edge xy joins
        # outer vertices x,y. L sets join to the first nonouter vertex n both
        # P(x) and P(y). Then it labels all nonouter vertices preceding join in
        # P(x) or P(y)

        r, s = self.FIRST[x], self.FIRST[y]
        if r == s:
            return

        self.setFlag(r, n_xy)

        # L1: switch paths
        while True:
            if s != 0:
                # r is flagged nonouter vertex, alternately in P(x) and P(y)
                r, s = s, r

            # L2: next nonouter vertex
            # r is set to the next nonouter vertex in P(x) or P(y)
            r = self.FIRST[self.LABEL[self.MATE[r]]]
            if self.isFlagged(r, n_xy):
                join = r
                break
            self.setFlag(r, n_xy)
            # go to L1

        # L3: label vertices in P(x), P(y)
        for v in (self.FIRST[x], self.FIRST[y]):
            # L4: label v
            while v != join:
                self.setLabel(v, n_xy)
                self.FIRST[v] = join
                v = self.FIRST[self.LABEL[self.MATE[v]]]
        # L5: update FIRST
        for i in self.outerVertices:
            if self.isOuterVertex(self.FIRST[i]):
                self.FIRST[i] = join

    def R(self, v, w):
        # R(v,w) rematches edges in the augmenting path. Vertex v is outer.
        # Part of path (w)*P(v) is in the augmenting path. It gets rematched
        # by R(v, w) (Although R sets MATE(v) <- w, it does not set
        # MATE(w) <- v. This is done in step E3 or another call to R)

        # R1: Match v to w
        t = self.MATE[v]
        self.MATE[v] = w
        if self.MATE[t] != v:
            # the path is completely rematched
            return

        # R2: Rematch a path
        if self.hasVertexLabel(v):
            self.MATE[t] = self.LABEL[v]
            self.R(self.LABEL[v], t)
            return

        # R3: Rematch two paths
        x, y = self.getEdge(self.LABEL[v])
        self.R(x, y)
        self.R(y, x)

    def E(self):
        # E constructs a maximum mathching on a graph. It starts a search for an
        # augmenting path to each unmatched vertex u. It scans edges of the
        # graph, deciding to assign new labels or to augment the matching

        for u in range(1, self.V + 1):
            # E1: Find an unmatched vertex
            if self.MATE[u] > 0:
                continue
            self.setLabel(u, 0)
            self.FIRST[u] = 0

            # E2: Choose an edge
            while True:
                x, n_xy = self.chooseAnEdge()
                if x is None:
                    # E7
                    self.stopTheSearch()
                    break
                edge = self.getEdge(n_xy)
                y = x ^ edge[0] ^ edge[1]

                # E3: augment the matching
                if not self.isMatched(y) and y != u:
                    self.MATE[y] = x
                    # R completes augmenting path along path (y)*P(x)
                    self.R(x, y)
                    # E7: stop the search
                    self.stopTheSearch()
                    break

                # E4: assign edge labels
                if self.isOuterVertex(y):
                    # L assigns edge label n(xy) to nonouter vertices in
                    #  P(x) and P(y)
                    self.L(x, y, n_xy)
                    continue

                # E5: Assign a  vertex label
                v = self.MATE[y]
                if not self.isOuterVertex(v):
                    self.setLabel(v, x)
                    self.FIRST[v] = y

                # E6: get next edge (continue looping)
