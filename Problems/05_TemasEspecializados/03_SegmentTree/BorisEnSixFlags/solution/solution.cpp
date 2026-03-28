#include <bits/stdc++.h>
using namespace std;

// --------------------------- Defines -------------------------------------  //
template<typename A, typename B> ostream& operator<<(ostream &os, const pair<A, B> &p) { return os << '(' << p.first << ", " << p.second << ')'; }
template<
    typename T_container, typename T = typename enable_if<!is_same<T_container, string>::value, typename T_container::value_type>::type
> ostream& operator<<(ostream &os, const T_container &v) { os << '{'; string sep; for (const T &x : v) os << sep << x, sep = ", "; return os << '}'; }
void dbg_out() { cerr << endl; }
template<typename Head, typename... Tail> void dbg_out(Head H, Tail... T) { cerr << ' ' << H; dbg_out(T...); }

#ifdef FILE_STREAM
streambuf *cin_backup = cin.rdbuf(), *cout_backup = cout.rdbuf();
ifstream f_in("name.in");
ofstream f_out("name.out");
#endif // FILE_STREAM

#ifdef DEBUG
    #define dbg(...) cerr << "(" << #__VA_ARGS__ << "):", dbg_out(__VA_ARGS__)
#else
    #define dbg(...)
#endif

#define ll long long
#define fill_array(x, y) memset(x, y, sizeof(x))
#define out_range_map(x,y) ((x) < 0 || (y) < 0 || (x) == N || (y) == M)
#define sza(x) ((int)x.size())
#define all(x) (x).begin(), (x).end()
#define fori(i, N) for(int i = 0; i < N; i++)
#define left(x) (x << 1 | 1)
#define right(x) (left(x) + 1)
#define half (l + r) / 2
// --------------------------- /Defines/ ------------------------------------ //

// --------------------------- Constants ----------------------------------- //
const ll LN = (ll)(1e5 + 5), 
         LM = (ll)(1e2 + 5), 
         INF = (ll)(1e15), 
         MOD = (ll)(1e9);
ll N, M, T, Q;
// -------------------------- /Constants/ ---------------------------------- //

template < typename T_1, typename T_2>
class ACST
{
protected:
	vector < T_1 > node;
	vector < T_2 > lazy;
	vector < T_1 > vec;
	vector < bool > pend;
	T_1 dflt_node;
	T_2 tval;
	int tl = 0, tr = 0, N = 0;
	bool init = false;

	bool out_range(int l, int r)
	{
		if (tl > r || tr < l)
			return true;
		return false;
	}

	bool in_range(int l, int r)
	{
		if (tl <= l && r <= tr)
			return true;
		return false;
	}

	virtual T_1 merge(T_1 l, T_1 r) = 0;

	virtual T_1 merge_range(int l, int r, T_1 node, T_2 lazy) = 0;

	virtual T_2 merge_lazy(T_2 lazy, T_2 upd) = 0;

	void propagate(int pos, int l, int r)
	{
		node[pos] = merge_range(l, r, node[pos], lazy[pos]);
		if (l != r)
		{
			lazy[left(pos)] = (pend[left(pos)] ? merge_lazy(lazy[left(pos)], lazy[pos]) : lazy[pos]);
			pend[left(pos)] = true;
			lazy[right(pos)] = (pend[right(pos)] ? merge_lazy(lazy[right(pos)], lazy[pos]) : lazy[pos]);
			pend[right(pos)] = true;
		}
		pend[pos] = false;
	}

	void _build(int pos, int l, int r)
	{
		pend[pos] = false;
		if (l == r)
		{
			node[pos] = vec[l] = (init ? vec[l] : dflt_node);
			return;
		}
		_build(left(pos), l, half);
		_build(right(pos), half + 1, r);
		node[pos] = merge(node[left(pos)], node[right(pos)]);
	}

	void _update(int pos, int l, int r)
	{
		if (pend[pos])
			propagate(pos, l, r);
		if (out_range(l, r))
			return;
		if (in_range(l, r))
		{
			lazy[pos] = tval;
			propagate(pos, l, r);
			return;
		}
		_update(left(pos), l, half);
		_update(right(pos), half + 1, r);
		node[pos] = merge(node[left(pos)], node[right(pos)]);
	}

	T_1 _query(int pos, int l, int r)
	{
		if (pend[pos])
			propagate(pos, l, r);
		if (out_range(l, r))
			return dflt_node;
		if (in_range(l, r))
			return node[pos];
		return merge(_query(left(pos), l, half), _query(right(pos), half + 1, r));
	}

public:

	virtual void build(int N, T_1 dflt_node, vector < T_1 > vec = vector < T_1 >())
	{
		this->N = N;
		this->dflt_node = dflt_node;
		if (vec.empty())
			(this->vec).resize(N);
		else
		{
			this->vec = vec;
			init = true;
		}

		node.resize(4 * N);
		lazy.resize(4 * N);
		pend.resize(4 * N);
		_build(0, 0, N - 1);
	}

	virtual void update(int l, int r, T_2 val)
	{
		tl = l;
		tr = r;
		tval = val;
		_update(0, 0, N - 1);
	}

	virtual T_1 query(int l, int r)
	{
		tl = l;
		tr = r;
		return _query(0, 0, N - 1);
	}

};


template < typename T_1, typename T_2 >
class CST : public ACST < T_1, T_2 >
{
    public:
        T_1 merge(T_1 l, T_1 r)
        {
            return l + r;
        }

        T_1 merge_range(int l, int r, T_1 node, T_2 lazy)
        {
            return node + lazy * (r - l + 1);
        }

        T_2 merge_lazy(T_2 lazy, T_2 upd)
        {
            return lazy + upd;
        }
};

// Use the vector pos to construct your ST
class HeavyLight {
    public:
        vector<vector<int>> tree, descomposition;
        int root, N, act_p;
        vector<int> parent, depth, heavy, head, pos;
        
        HeavyLight(){}
        HeavyLight(int root_, vector<vector<int>>& tree_) {init(root_, tree_);}

        void init(int root_, vector<vector<int>>& tree_) {
            root = root_;
            tree = tree_;
            N = tree.size();

            parent.resize(N, root);
            depth.resize(N);
            heavy.resize(N, -1);
            head.resize(N);
            pos.resize(N);
            act_p = 0;

            dfs(root);
            decompose(root, root);

            return;
        }

        int dfs(int v) {
            int size = 1,
                max_c_size = 0,
                c_size;

            for (int c : tree[v]) {
                if (c != parent[v]) {
                    parent[c] = v, depth[c] = depth[v] + 1;
                    c_size = dfs(c);
                    size += c_size;
                    if (c_size > max_c_size)
                        max_c_size = c_size, heavy[v] = c;
                }
            }

            return size;
        }

        void decompose(int v, int h) {
            head[v] = h, pos[v] = act_p++;
            if (heavy[v] != -1)
                decompose(heavy[v], h);
            for (int c : tree[v]) {
                if (c != parent[v] && c != heavy[v])
                    decompose(c, c);
            }
        }

        vector<pair<int, int>> query(int a, int b) {
            int res = 0;
            vector<pair<int, int>> queries;

            for (; head[a] != head[b]; b = parent[head[b]]) {
                if (depth[head[a]] > depth[head[b]])
                    swap(a, b);
                queries.push_back({pos[head[b]], pos[b]});
            }

            if (depth[a] > depth[b])
                swap(a, b);

            // --- LCA included --- //
            queries.push_back({pos[a], pos[b]});
            
            return queries;
        }
};

// ------------------------- Your code ---------------------------------- //
void Solve() {
	cin >> N;
    vector<vector<int>> adj(N);
    vector<ll> vals(N), n_vals(N);

    for(auto& ai: vals)
        cin >> ai;

    for (int i = 0; i < N-1; i++) {
        int u, v;
        cin >> u >> v;
        u--, v--;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    cin >> M;

    HeavyLight hld(0, adj);
    for (int i = 0; i < N; i++)
        n_vals[hld.pos[i]] = vals[i];

    CST<ll, ll> st;
    st.build(N, 0, n_vals);
    
    while (M--)
    {
        char tp; int a, b;
        cin >> tp >> a >> b;
        a--;
        if (tp == '+') {
            int pos = hld.pos[a];
            int x = vals[a] - b;
            vals[a] = b;
            st.update(pos, pos, x);
        } else {
            b--;
            auto queries = hld.query(a, b);
            ll ans = 0;
            for (auto& [l, r]: queries)
                ans += st.query(l, r);
            cout << ans << '\n';
        }
    }
    
}
// --------------------------------------------------------------------- //

int main() {
    #ifdef DEBUG
        freopen("input.txt","w",stdin);
        freopen("output.txt","w",stdout);
    #else
        ios_base::sync_with_stdio(0); cin.tie(0);
    #endif

    int Tc = 1;
   // cin >> Tc;

    fori(i, Tc)
        Solve();

    return 0;
}
