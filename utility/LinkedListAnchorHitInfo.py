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
            min_hits = max(self.max_hit, min_hits)
        while current:
            if current.hits < min_hits:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
            current = current.next

    def combine_groups(self):
        current = self.head
        prev = None
        while current.next:
            prev = current
            current = prev.next

            if (current.hits == 0) or (prev.hits == 0):
                continue
            hits_intersection = prev.hit_ids.intersection(current.hit_ids)
            if hits_intersection:
                continue

            hits_union = prev.hit_ids.union(current.hit_ids)
            hits = len(hits_union)
            if self.max_hit < hits:
                self.max_hit = hits
            page_nums = prev.page_nums + current.page_nums

            nn = Node(prev.prev, page_nums, hits, hits_union)
            prev.prev.next = nn
            current.next.prev = nn
            nn.next = current.next
            current = nn
