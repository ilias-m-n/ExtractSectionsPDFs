class Node:
    def __init__(self, prev, page_num, hits, hit_ids):
        self.page_nums = page_num if isinstance(page_num, list) else [page_num]
        self.hits = hits
        self.hit_ids = hit_ids
        self.prev = prev
        self.next = None

    def __str__(self):
        return f"Pages {self.page_nums}, Hits {self.hits}, Hit IDs {self.hit_ids}"


class LinkedListAnchorHitInfo:
    def __init__(self):
        self.head = None
        self.max_hit = 0

    def append(self, page_num, hits, hit_ids):
        if self.head is None:
            self.head = Node(None, page_num, hits, hit_ids)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(current, page_num, hits, hit_ids)
        if self.max_hit < hits:
            self.max_hit = hits


    def build_from_list(self, nodes: list):
        self.head = None
        for node in nodes:
            self.append(*node)


    def print(self):
        current = self.head
        while current:
            print(current)
            current = current.next
        print('End')

    def to_dict(self):
        result_dict = {}
        current = self.head
        while current:
            result_dict[tuple(current.page_nums)] = current.hits
            current = current.next
        return result_dict

    def remove_below_min_hits(self, min_hits, flag_only_max):
        current = self.head
        if flag_only_max:
            min_hits = self.max_hit
        min_hits = min(min_hits, self.max_hit)
        while current:
            if current.hits < min_hits:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
            current = current.next

    def combine_groups(self, flag_allow_duplicate_hit_ids = False):
        current = self.head
        prev = None
        while current.next:
            prev = current
            current = prev.next

            if (current.hits == 0) or (prev.hits == 0):
                continue
            hits_intersection = prev.hit_ids.intersection(current.hit_ids)
            if hits_intersection and not flag_allow_duplicate_hit_ids:
                continue

            hits_union = prev.hit_ids.union(current.hit_ids)
            hits = len(hits_union)
            if self.max_hit < hits:
                self.max_hit = hits
            page_nums = prev.page_nums + current.page_nums

            nn = Node(prev.prev, page_nums, hits, hits_union)
            if prev != self.head:
                prev.prev.next = nn
            else:
                self.head = nn
            if current.next:
                current.next.prev = nn
            nn.next = current.next
            current = nn

    def combine_skip_groups(self, flag_allow_duplicate_hit_ids = False):
        current = self.head
        prev = None
        pprev = None

        flag_first_run = True

        while current and current.next and current.next.next:
            if flag_first_run:
                pprev = current
                prev = current.next
                current = current.next.next
                flag_first_run = False
            else:
                pprev = prev
                prev = current
                current = current.next

            # print(pprev.hit_ids, prev.hit_ids, current.hit_ids)

            if (current.hits == 0) or (pprev.hits == 0):
                continue
            skip_hits_intersection = pprev.hit_ids.intersection(current.hit_ids)
            if skip_hits_intersection and not flag_allow_duplicate_hit_ids:
                continue

            hits_union = pprev.hit_ids.union(current.hit_ids)
            hits = len(hits_union)
            if self.max_hit < hits:
                self.max_hit = hits
            page_nums = pprev.page_nums + prev.page_nums + current.page_nums

            nn = Node(pprev.prev, page_nums, hits, hits_union)

            if pprev != self.head:
                pprev.prev.next = nn
            else:
                self.head = nn
            if current.next:
                current.next.prev = nn
            nn.next = current.next
            current = nn

    def fix_overlaying_sections(self, ll_other):
        c = self.head
        co = ll_other.head
        while c:
            if c.hits == 0 or co.hits == 0:
                c = c.next
                co = co.next
                continue
            if c.hits > co.hits:
                co.hits = 0
                co.hit_ids = []
            elif c.hits < co.hits:
                c.hits = 0
                c.hit_ids = []
            c = c.next
            co = co.next

