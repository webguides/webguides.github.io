module TocGenerator
  class Generator < Jekyll::Generator
    safe true
    priority :low
    
    def generate(site)
      site.posts.docs.each do |post|
        post.data['toc'] = true
        content = post.content
        toc_html = ""
        
        # Simple regex for headers
        content.gsub!(/<h2 id="([^"]+)">([^<]+)<\/h2>/) do
          "<h2 id=\"#{$1}\"><a href=\"#$1\">#{$2}</a></h2>"
        end
        
        content.gsub!(/<h3 id="([^"]+)">([^<]+)<\/h3>/) do
          "<h3 id=\"#{$1}\"><a href=\"#$1\">#{$2}</a></h3>"
        end
        
        # Build TOC
        toc_items = []
        content.scan(/<h[2-3] id="([^"]+)">/) do |id|
          title = content.scan(/<h[2-3] id="#{id[0]}"[^>]*>([^<]+)</)[0][1]
          level = content.scan(/<h([2-3]) id="#{id[0]}"/)[0][1].to_i
          toc_items << { id: id[0], title: title, level: level }
        end
        
        if toc_items.any?
          toc_html = "<div class='toc'><h3>Contents</h3><ul>"
          toc_items.each do |item|
            toc_html += "<li><a href='##{item[:id]}'>#{item[:title]}</a></li>"
          end
          toc_html += "</ul></div>"
          post.content = toc_html + "\n\n" + content
        end
      end
    end
  end
end
