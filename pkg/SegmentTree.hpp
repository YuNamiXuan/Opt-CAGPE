#include <vector>
#include <cassert>

struct SegTreeNode
{
    int val = 0;
    int max_val = 0;
    int val_2 = -1;
};

class SegmentTree
{
public:
    SegmentTree(int len, int val);

    void update(int pos, int val);
    void update_id(int id, int val, int val2);
    int query_first_larger(int val);
    int get_val(int id);
    int get_val2(int id);

private:
    int length;
    std::vector<SegTreeNode> nodes;
    void _update(int id, int l, int r, int pos, int val);
    void maintain(int id);
};

SegmentTree::SegmentTree(int len, int val)
    : length(len),
      nodes(std::vector<SegTreeNode>(len << 2))
{
    for (auto &node : nodes)
    {
        node.val = val;
        node.max_val = val;
    }
}

int SegmentTree::get_val(int id)
{
    if (id >= nodes.size())
        return -1;
    return nodes[id].val;
}

int SegmentTree::get_val2(int id)
{
    if (id >= nodes.size())
        return -1;
    return nodes[id].val_2;
}

int SegmentTree::query_first_larger(int val)
{
    if (nodes[1].max_val < val)
        return -1;

    int id = 1;
    int l = 0, r = length;

    while (r - l > 1)
    {
        int mid = (l + r) >> 1;
        if (nodes[id << 1].max_val >= val)
        {
            r = mid;
            id = id << 1;
        }
        else
        {
            l = mid;
            id = (id << 1) + 1;
        }
    }

    return id;
}

void SegmentTree::maintain(int id)
{
    if ((id << 1) >= nodes.size())
        return;
    nodes[id].max_val =
        std::max(nodes[id << 1].max_val, nodes[(id << 1) + 1].max_val);
}

void SegmentTree::update_id(int id, int val, int val2)
{
    if (id >= nodes.size())
        return;
    nodes[id].val = val;
    nodes[id].max_val = val;
    nodes[id].val_2 = val2;
    id = id >> 1;

    while (id > 0)
    {
        maintain(id);
        id = id >> 1;
    }
}

void SegmentTree::_update(int id, int l, int r, int pos, int val)
{
    if (r - l == 1)
    {
        assert(l == pos);
        nodes[id].val = val;
        nodes[id].max_val = val;
        return;
    }

    int mid = (l + r) >> 1;
    if (pos < mid)
    {
        _update(id << 1, l, mid, pos, val);
    }
    else
    {
        _update((id << 1) + 1, mid, r, pos, val);
    }

    maintain(id);
}

void SegmentTree::update(int pos, int val) { _update(1, 0, length, pos, val); }
